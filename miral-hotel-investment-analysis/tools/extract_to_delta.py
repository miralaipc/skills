"""
Miral Hotel Analysis — Document Extractor
==========================================
Runs on GitHub Actions (NOT on Databricks).
Has full internet access — downloads PDFs from GitHub,
extracts text, writes rows to Databricks Delta table
via the Databricks SQL connector.

No Spark. No dbutils. No cluster internet access needed.

Environment variables (set as GitHub Actions secrets):
  GITHUB_PAT           — GitHub PAT with repo read access
  DATABRICKS_HOST      — https://adb-3821540461636682.2.azuredatabricks.net
  DATABRICKS_TOKEN     — Databricks personal access token
  DATABRICKS_HTTP_PATH — /sql/1.0/warehouses/9a7124860d81a5c1

Tables written:
  ml_dev.dev_schema.knowledge_base
  ml_dev.dev_schema.extraction_log
"""

import os
import sys
import json
import hashlib
import tempfile
import requests
import pandas as pd
from datetime import datetime, timezone
from pathlib import Path
from pdfminer.high_level import extract_text
from databricks import sql as dbsql

# ── Config ────────────────────────────────────────────────────────────────────

GITHUB_OWNER   = "miralaipc"
GITHUB_REPO    = "skills"
GITHUB_BRANCH  = "main"
DOCUMENTS_BASE = "miral-hotel-investment-analysis/documents"

UC_CATALOG = "ml_dev"
UC_SCHEMA  = "dev_schema"
KB_TABLE   = f"{UC_CATALOG}.{UC_SCHEMA}.knowledge_base"
LOG_TABLE  = f"{UC_CATALOG}.{UC_SCHEMA}.extraction_log"

FOLDER_SECTION_MAP = {
    "Brands":                           "brands",
    "DCT":                              "dct",
    "Future Reports":                   "future-reports",
    "STR Industry Data/Cluster STR":    "str-cluster-data",
    "STR Industry Data":                "str-industry-data",
    "USALI Hotel Accounting Standards": "usali-standards",
}

# ── Read environment variables ────────────────────────────────────────────────

GITHUB_PAT           = os.environ.get("GITHUB_PAT", "")
DATABRICKS_HOST      = os.environ.get("DATABRICKS_HOST", "")
DATABRICKS_TOKEN     = os.environ.get("DATABRICKS_TOKEN", "")
DATABRICKS_HTTP_PATH = os.environ.get("DATABRICKS_HTTP_PATH", "")

for var, val in [
    ("GITHUB_PAT",           GITHUB_PAT),
    ("DATABRICKS_HOST",      DATABRICKS_HOST),
    ("DATABRICKS_TOKEN",     DATABRICKS_TOKEN),
    ("DATABRICKS_HTTP_PATH", DATABRICKS_HTTP_PATH),
]:
    if not val:
        print(f"ERROR: Environment variable '{var}' is not set.")
        sys.exit(1)

# ── Databricks SQL connection ─────────────────────────────────────────────────

def get_conn():
    return dbsql.connect(
        server_hostname = DATABRICKS_HOST.replace("https://", ""),
        http_path       = DATABRICKS_HTTP_PATH,
        access_token    = DATABRICKS_TOKEN,
    )


def run_sql(sql: str, params: list = None):
    """Execute SQL — no return value (CREATE, INSERT, MERGE etc.)"""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or [])


def run_query(sql: str, params: list = None) -> list[dict]:
    """Execute SQL and return rows as list of dicts."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or [])
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]

# ── GitHub helpers ────────────────────────────────────────────────────────────

def gh_headers() -> dict:
    return {
        "Authorization": f"Bearer {GITHUB_PAT}",
        "Accept":        "application/vnd.github+json",
    }


def list_folder_recursive(api_url: str) -> list[dict]:
    resp = requests.get(api_url, headers=gh_headers(), timeout=30)
    resp.raise_for_status()
    files = []
    for item in resp.json():
        if item["type"] == "file":
            files.append(item)
        elif item["type"] == "dir":
            files.extend(list_folder_recursive(item["url"]))
    return files


def download_file(url: str, dest: Path):
    resp = requests.get(
        url,
        headers={"Authorization": f"Bearer {GITHUB_PAT}"},
        timeout=60,
        stream=True,
    )
    resp.raise_for_status()
    dest.write_bytes(resp.content)

# ── Extraction helpers ────────────────────────────────────────────────────────

def extract_pdf(path: Path) -> str:
    try:
        text = extract_text(str(path)).strip()
        return text if text else "[No extractable text — possibly scanned PDF]"
    except Exception as e:
        return f"[PDF extraction failed: {e}]"


def extract_xlsx(path: Path) -> list[dict]:
    try:
        sheets = pd.read_excel(path, sheet_name=None, dtype=str)
        return [
            {
                "sheet_name": name,
                "content":    df.dropna(how="all").fillna("").to_markdown(index=False),
            }
            for name, df in sheets.items()
        ]
    except Exception as e:
        return [{"sheet_name": "error", "content": f"[Excel extraction failed: {e}]"}]


def assign_section(file_path: str) -> str | None:
    relative = file_path.replace(f"{DOCUMENTS_BASE}/", "")
    for key in sorted(FOLDER_SECTION_MAP.keys(), key=len, reverse=True):
        if relative.startswith(key + "/"):
            return FOLDER_SECTION_MAP[key]
    return None

# ── Delta table setup ─────────────────────────────────────────────────────────

def ensure_tables():
    print("  Creating tables if they don't exist...")

    run_sql(f"""
        CREATE TABLE IF NOT EXISTS {KB_TABLE} (
            id            STRING    NOT NULL,
            section       STRING    NOT NULL,
            source_folder STRING    NOT NULL,
            github_path   STRING    NOT NULL,
            filename      STRING    NOT NULL,
            file_type     STRING    NOT NULL,
            sheet_name    STRING,
            content       STRING    NOT NULL,
            file_sha      STRING    NOT NULL,
            extracted_at  TIMESTAMP NOT NULL
        )
        USING DELTA
        PARTITIONED BY (section)
    """)

    run_sql(f"""
        CREATE TABLE IF NOT EXISTS {LOG_TABLE} (
            run_id          STRING    NOT NULL,
            started_at      TIMESTAMP NOT NULL,
            completed_at    TIMESTAMP NOT NULL,
            files_processed STRING    NOT NULL,
            files_failed    STRING    NOT NULL,
            files_skipped   STRING    NOT NULL,
            status          STRING    NOT NULL,
            notes           STRING
        )
        USING DELTA
    """)
    print(f"  ✓ {KB_TABLE}")
    print(f"  ✓ {LOG_TABLE}")

# ── Upsert rows ───────────────────────────────────────────────────────────────

def upsert_rows(rows: list[dict]):
    """
    Upsert rows into knowledge_base using MERGE.
    Only updates rows where file_sha has changed.
    Batches in groups of 50 to avoid SQL statement size limits.
    """
    if not rows:
        return

    BATCH = 50
    for i in range(0, len(rows), BATCH):
        batch = rows[i:i + BATCH]

        # Build VALUES string
        values = []
        for r in batch:
            sheet = f"'{r['sheet_name']}'" if r["sheet_name"] else "NULL"
            # Escape single quotes in content
            content = r["content"].replace("'", "''")
            values.append(
                f"('{r['id']}', '{r['section']}', '{r['source_folder']}', "
                f"'{r['github_path']}', '{r['filename']}', '{r['file_type']}', "
                f"{sheet}, '{content}', '{r['file_sha']}', "
                f"CAST('{r['extracted_at']}' AS TIMESTAMP))"
            )

        values_sql = ",\n".join(values)

        run_sql(f"""
            MERGE INTO {KB_TABLE} AS target
            USING (
                SELECT * FROM (VALUES
                    {values_sql}
                ) AS t(id, section, source_folder, github_path, filename,
                        file_type, sheet_name, content, file_sha, extracted_at)
            ) AS source ON target.id = source.id
            WHEN MATCHED AND target.file_sha != source.file_sha THEN UPDATE SET
                content      = source.content,
                file_sha     = source.file_sha,
                extracted_at = source.extracted_at
            WHEN NOT MATCHED THEN INSERT *
        """)
        print(f"  Upserted batch {i // BATCH + 1} ({len(batch)} rows)")


def delete_removed_files(current_paths: set[str]):
    """Delete rows for files no longer in GitHub."""
    existing = run_query(f"SELECT DISTINCT github_path FROM {KB_TABLE}")
    existing_paths = {r["github_path"] for r in existing}
    removed = existing_paths - current_paths

    if removed:
        paths_list = ", ".join(f"'{p}'" for p in removed)
        run_sql(f"DELETE FROM {KB_TABLE} WHERE github_path IN ({paths_list})")
        print(f"  Deleted {len(removed)} rows for removed files: {removed}")
    else:
        print("  No files removed.")

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    run_id  = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    started = datetime.now(timezone.utc)
    print(f"=== Miral Extraction — Run {run_id} ===\n")

    print("Step 1: Setting up Delta tables...")
    ensure_tables()
    print()

    print("Step 2: Discovering files in GitHub documents/...")
    root_url  = (
        f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}"
        f"/contents/{DOCUMENTS_BASE}?ref={GITHUB_BRANCH}"
    )
    all_files = list_folder_recursive(root_url)
    print(f"  Found {len(all_files)} file(s)\n")

    processed, skipped, failed = [], [], []
    rows = []
    now  = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    print("Step 3: Downloading and extracting...")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        for item in all_files:
            filepath     = item["path"]
            filename     = item["name"]
            file_sha     = item["sha"]
            download_url = item["download_url"]
            suffix       = Path(filename).suffix.lower()

            section = assign_section(filepath)
            if section is None:
                skipped.append(filepath)
                print(f"  SKIP (unmapped): {filepath}")
                continue

            source_folder = filepath.replace(f"{DOCUMENTS_BASE}/", "").split("/")[0]
            local         = tmp_path / filename

            print(f"  Downloading: {filename}")
            try:
                download_file(download_url, local)
            except Exception as e:
                failed.append(filepath)
                print(f"    ERROR: {e}")
                continue

            if suffix == ".pdf":
                content = extract_pdf(local)
                row_id  = hashlib.sha256(filepath.encode()).hexdigest()[:16]
                rows.append({
                    "id":            row_id,
                    "section":       section,
                    "source_folder": source_folder,
                    "github_path":   filepath,
                    "filename":      filename,
                    "file_type":     "pdf",
                    "sheet_name":    None,
                    "content":       content,
                    "file_sha":      file_sha,
                    "extracted_at":  now,
                })
                processed.append(filepath)

            elif suffix in (".xlsx", ".xls"):
                sheets = extract_xlsx(local)
                for sheet in sheets:
                    row_id = hashlib.sha256(
                        f"{filepath}::{sheet['sheet_name']}".encode()
                    ).hexdigest()[:16]
                    rows.append({
                        "id":            row_id,
                        "section":       section,
                        "source_folder": source_folder,
                        "github_path":   filepath,
                        "filename":      filename,
                        "file_type":     "xlsx",
                        "sheet_name":    sheet["sheet_name"],
                        "content":       sheet["content"],
                        "file_sha":      file_sha,
                        "extracted_at":  now,
                    })
                processed.append(filepath)
            else:
                skipped.append(filepath)

    print(f"\nStep 4: Upserting {len(rows)} row(s) into {KB_TABLE}...")
    upsert_rows(rows)

    print(f"\nStep 5: Removing deleted files...")
    delete_removed_files({f["path"] for f in all_files})

    # Write extraction log
    completed = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    notes     = f"Failed: {failed}" if failed else None
    notes_sql = f"'{notes}'" if notes else "NULL"

    run_sql(f"""
        INSERT INTO {LOG_TABLE}
        VALUES (
            '{run_id}',
            CAST('{started.strftime("%Y-%m-%d %H:%M:%S")}' AS TIMESTAMP),
            CAST('{completed}' AS TIMESTAMP),
            '{len(processed)}',
            '{len(failed)}',
            '{len(skipped)}',
            '{"SUCCESS" if not failed else "PARTIAL"}',
            {notes_sql}
        )
    """)

    print(f"\n{'='*40}")
    print(f"✓ Done — Processed: {len(processed)} | Skipped: {len(skipped)} | Failed: {len(failed)}")
    if failed:
        print(f"  Failed: {failed}")
        sys.exit(1)


if __name__ == "__main__":
    main()
