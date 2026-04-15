---
name: miral-hotel-investment-analysis
description: >
  Generates professional hotel investment analysis reports and HTML presentation
  pages for Miral's hotel portfolio on Yas Island and Saadiyat Island, Abu Dhabi.
  Use when the user provides a Miral hotel name or asks to analyze, benchmark,
  underwrite, or report on any hotel asset within Miral's ecosystem. Triggers for
  RevPAR benchmarking, ADR analysis, occupancy trends, investment committee memos,
  cap rate or IRR modeling, or any UAE hotel investment analysis. Always use this
  skill when the user mentions The WB Abu Dhabi, Hilton Yas Island, Crowne Plaza
  Yas Island, W Abu Dhabi, Radisson Blu Yas Island, Yas Island Rotana, Centro Yas
  Island, Park Inn Yas Island, DoubleTree Yas Island, or Staybridge Suites.
---

# Miral Hotel Investment Analysis

Generates professional hotel investment analysis reports and HTML display pages
for Miral's hotel portfolio on Yas Island and Saadiyat Island, Abu Dhabi — based
on real-time documents fetched from the Miral GitHub knowledge base.

The analysis is executed in two steps:
- **Step 1**: Generate a detailed investment analysis report (P1–P9, 19 pages total)
- **Step 2**: Generate an HTML display page (viewable in browser, printable as PDF)

---

## Task Objectives

- Automatically select the correct hotel profile and comp set based on the target hotel
- Fetch latest market data, benchmarks, and financial assumptions from GitHub
- Generate complete analysis content following the P1–P9 template structure (19 pages)
- Provide KPI benchmarks across 5 key indices: occupancy, ADR, RevPAR, GOPPAR, GOP margin
- Provide detailed investment models (revenue, cost, cap rate, IRR, payback period)
- Provide data source annotations and investment recommendations
- Generate HTML display page (viewable in browser, printable as PDF)

---

## Step 0 — Fetch Knowledge Base from GitHub (Always Do First)

### Step 0 — Read PAT First

```bash
cat ~/.claude/CLAUDE.md
# Extract the value after "GITHUB_PAT: "
```

Store as `PAT` for all subsequent requests.

### Repository Details
```
Owner  : miralaipc
Repo   : skills
Branch : main
Base   : miral-hotel-investment-analysis/documents
Access : Private — PAT required
```

### Document Structure

```
documents/
├── Brands/                          # Brand fee schedules, PIP standards, management contracts
├── DCT/                             # DCT Abu Dhabi tourism reports, visitor statistics
├── Future Reports/                  # Pipeline and forward-looking market analyses
├── STR Industry Data/               # STR UAE market benchmarks (PDFs)
│   └── Cluster STR/                 # Cluster-level STR data (.xlsx files)
└── USALI Hotel Accounting Standards/ # USALI P&L standards, departmental accounting
```

All files are **PDF** except `STR Industry Data/Cluster STR/` which contains **`.xlsx`** files.

---

### Step 0a — Discover Documents (Recursive)

List each folder via the GitHub Contents API. Repeat for subfolders when found.

```python
import subprocess, json

BASE = "https://api.github.com/repos/miralaipc/skills/contents/miral-hotel-investment-analysis/documents"
PAT = "<value read from ~/.claude/CLAUDE.md>"
HEADERS = [
    f"Authorization: Bearer {PAT}",
    "Accept: application/vnd.github+json"
]

def list_folder(path):
    result = subprocess.run(
        ["curl", "-s", path] + [h for header in HEADERS for h in ["-H", header]],
        capture_output=True, text=True
    )
    items = json.loads(result.stdout)
    files, dirs = [], []
    for item in items:
        if item["type"] == "file":
            files.append({"name": item["name"], "download_url": item["download_url"], "path": item["path"]})
        elif item["type"] == "dir":
            dirs.append(item["url"])
    return files, dirs

all_files = []
queue = [BASE]
while queue:
    url = queue.pop()
    files, subdirs = list_folder(url)
    all_files.extend(files)
    queue.extend(subdirs)
```

This discovers all PDFs and .xlsx files recursively, including `Cluster STR/`.

---

### Step 0b — Select Relevant Documents

| Task involves | Fetch from folder |
|---|---|
| Occupancy, ADR, RevPAR, comp set, STR benchmarks | `STR Industry Data/` + `STR Industry Data/Cluster STR/` |
| Tourism stats, visitor numbers, seasonality, demand | `DCT/` |
| Brand fees, PIP obligations, franchise costs | `Brands/` |
| GOP, GOPPAR, departmental margins, P&L structure | `USALI Hotel Accounting Standards/` |
| Pipeline supply, future market scenarios | `Future Reports/` |
| Full investment analysis or IC memo | **All folders** |

Filter `all_files` by folder path to fetch only what is needed.

---

### Step 0c — Download and Extract Content

#### PDFs — extract text with Python

```bash
pip install pdfminer.six --quiet
```

```python
import urllib.request, os
from pdfminer.high_level import extract_text

def fetch_pdf_text(file_info, pat, tmp_dir="/tmp/miral_docs"):
    os.makedirs(tmp_dir, exist_ok=True)
    local_path = os.path.join(tmp_dir, file_info["name"])
    req = urllib.request.Request(
        file_info["download_url"],
        headers={"Authorization": f"Bearer {pat}"}
    )
    with urllib.request.urlopen(req) as r:
        with open(local_path, "wb") as f:
            f.write(r.read())
    return extract_text(local_path)
```

#### Excel files (.xlsx) — read with pandas

```python
import pandas as pd

def fetch_xlsx(file_info, pat, tmp_dir="/tmp/miral_docs"):
    os.makedirs(tmp_dir, exist_ok=True)
    local_path = os.path.join(tmp_dir, file_info["name"])
    req = urllib.request.Request(
        file_info["download_url"],
        headers={"Authorization": f"Bearer {pat}"}
    )
    with urllib.request.urlopen(req) as r:
        with open(local_path, "wb") as f:
            f.write(r.read())
    sheets = pd.read_excel(local_path, sheet_name=None)  # all sheets
    return {name: df.to_string() for name, df in sheets.items()}
```

Process only the files selected in Step 0b. Skip any file that fails — log the
filename and flag it `[FETCH FAILED — verify manually]`.

---

### Step 0d — Confirm to User

> *"Fetched [N] documents from GitHub: [list filenames]. Proceeding with analysis."*

List each filename and its source folder so the user can verify coverage.

---

### Error Handling

| Scenario | Action |
|---|---|
| PAT not found in CLAUDE.md | Ask user to add `GITHUB_PAT: ghp_xxx` to `~/.claude/CLAUDE.md` |
| 401 Unauthorized | PAT expired — regenerate at github.com/settings/tokens |
| 404 Not Found | Check repo path and branch; confirm repo is private and PAT has `repo` scope |
| API returns empty folder | Note folder as empty — proceed with other folders |
| PDF text extraction fails | Log filename; use `[VERIFY]` for any data from that source |
| Excel parse fails | Log filename; request user to paste key figures manually |
| Network timeout | Retry once; if still failing, proceed with built-in knowledge and flag all figures `[VERIFY]` |

---

## Inputs to Gather

- **Hotel name**: which Miral hotel to analyze (see portfolio below)
- **Analysis type**: acquisition / benchmarking / underwriting / IC memo / full report
- **Operating data**: T12 and 3–5 year P&L if available, STR UAE report,
  revenue segmentation (leisure transient, GCC domestic, international, group, contract)
- **Capital stack**: acquisition price or book value, debt terms, FF&E reserve,
  PIP obligations in AED
- **Market data**: comp set performance, new supply pipeline, event calendar impact

---

## Miral Hotel Portfolio

**Do not rely on any hardcoded hotel list.** All hotel names, brands, star
ratings, room counts, and ownership categories must be read from the fetched
documents in Step 0 — specifically from `Brands/` (brand profiles and management
contracts) and `Future Reports/` (supply pipeline). Cross-reference with
`STR Industry Data/` for room count confirmation.

When building the portfolio table for any analysis, construct it dynamically
from the fetched documents and cite the source filename next to each property
row. If a detail is not found in any document, mark it `[VERIFY]` rather than
filling it in from assumption or prior knowledge.

---

## Execution Process

### Step 1 — Identify Hotel and Select Profile

- Confirm target hotel name and analysis type from user
- Identify hotel category: Miral-owned / Yas Plaza cluster / Third-party on Miral land
- Load hotel profile and recommended comp set from fetched `Brands/` documents
- Load market benchmarks from fetched `STR Industry Data/` + `DCT/` documents
- Load financial P&L structure from fetched `USALI Hotel Accounting Standards/` documents

### Step 2 — Data Collection and Annotation

**Hotel KPI data:**
- Occupancy, ADR, RevPAR — from `STR Industry Data/` (PDFs) and `Cluster STR/` (.xlsx)
- GOPPAR, GOP margin — from `USALI Hotel Accounting Standards/` + user-provided P&L
- Theme park attachment rate — unique to Miral assets; cross-reference with `DCT/`

**Market data:**
- Yas Island / Saadiyat Island comp set performance — from `STR Industry Data/`
- New supply pipeline — from `Future Reports/`
- Key demand drivers: F1 Grand Prix, Etihad Arena events, Disneyland Abu Dhabi pipeline
- Seasonality: Peak Oct–Apr | Shoulder May, Sep | Low Jun–Aug — from `DCT/`

**Financial data:**
- Brand fee structures, PIP per key — from `Brands/`
- UAE VAT: 5% | DTCM municipality fee: 4–6% of room revenue
- AED pegged at 3.6725 per USD
- Cap rates, IRR ranges, DCF assumptions — derived from fetched benchmarks

**Data annotation**: mark all figures with `[source: filename]` at end of each page.
Missing data: use `≈` with estimation logic clearly stated.

---

## Report Template (P1–P9)

### P1: Abu Dhabi & Yas Island Macro Overview
**Title**: Steady tourism growth creates strong foundation for Yas Island hotels
- GDP growth, Abu Dhabi Tourism Strategy 2030, visitor numbers — from `DCT/`
- Yas Island visitor figures, YoY growth — from `DCT/` [do not hardcode figures; read from documents]
- Table: Key macro indicators with YoY growth
- Insight: one-sentence summary
- Source: DCT Abu Dhabi (from `DCT/`), Miral press releases

### P2: Demand Drivers Analysis
**Title**: Theme park ecosystem and events calendar drive year-round hotel demand
- Theme parks: Ferrari World, Warner Bros. World, SeaWorld, Yas Waterworld
- Events: F1 Grand Prix (Nov), Etihad Arena concerts, UFC, NBA
- Pipeline: Disneyland Abu Dhabi (7th Disney resort, announced May 2025)
- Park-stay bundle: 1 night = 1 complimentary park entry — unique demand driver
- Table: Annual events calendar with occupancy/ADR impact
- Insight: one-sentence summary
- Source: DCT Abu Dhabi (from `DCT/`), Miral, Formula 1

### P3: Hotel Market Supply Analysis
**Title**: Controlled supply with strong demand creates compelling investment case
- Total inventory, grade distribution — read from `STR Industry Data/` and `Future Reports/`; do not hardcode figures
- Pipeline keys and target year — read from `Future Reports/`
- Table: Hotel inventory by brand, stars, rooms, category (built from fetched documents)
- Insight: one-sentence summary
- Source: `Future Reports/`, STR UAE

### P4: Hotel Performance Benchmarks
**Title**: Yas Island hotels outperform Abu Dhabi market on all key KPIs
- Occupancy, ADR, RevPAR actuals — read from `STR Industry Data/` (PDFs + Cluster STR .xlsx); do not hardcode figures
- Saadiyat Island benchmarks — read from `STR Industry Data/`
- Abu Dhabi market RevPAR growth — read from `STR Industry Data/` or `DCT/`
- Table: Occupancy / ADR / RevPAR / GOPPAR / GOP margin — actuals vs. benchmarks
- Insight: one-sentence summary
- Source: `STR Industry Data/` (PDFs + Cluster STR .xlsx), DCT Abu Dhabi

### P5: Comp Set and Competitive Positioning
**Title**: Subject hotel positioned within a clearly defined competitive set
- Comp set definition for target hotel (from `Brands/` and `STR Industry Data/`)
- RevPAR Index (RGI) vs. comp set — RGI > 100 = outperformance
- OTA dependency: flag if > 25–30% of transient revenue
- Table: Subject hotel vs. comp set — Occupancy / ADR / RevPAR / RGI
- Insight: one-sentence summary
- Source: `STR Industry Data/Cluster STR/` (.xlsx — primary), STR UAE PDFs

### P6-1: Revenue Segmentation Analysis
**Title**: Diversified revenue base with theme park bundle as structural advantage
- Segments: leisure transient / GCC domestic / international / group & MICE / contract
- GCC domestic feeder markets — read from `DCT/`
- International source market growth figures — read from `DCT/`; do not hardcode percentages
- Table: Revenue segmentation breakdown with % contribution
- Insight: one-sentence summary
- Source: `DCT/`, user-provided P&L

### P6-2: Operating Efficiency Analysis
**Title**: Labour and FF&E benchmarks reveal operational improvement opportunities
- P&L structure per USALI standards (from `USALI Hotel Accounting Standards/`)
- Labour cost % by service level — read from `USALI Hotel Accounting Standards/`; do not hardcode ranges
- Departmental margin benchmarks (Rooms, F&B, Spa) — read from `USALI Hotel Accounting Standards/`
- FF&E reserve standard — read from `USALI Hotel Accounting Standards/` or `Brands/`
- PIP exposure per key by brand — read from `Brands/`
- Table: Operating cost benchmarks vs. actuals
- Insight: one-sentence summary
- Source: `USALI Hotel Accounting Standards/`, `Brands/`

### P7-1: Investment Model — Parameters
**Title**: Conservative assumptions anchored to verified Yas Island benchmarks
- Room revenue: Available rooms × 365 × Occupancy × ADR
- Total revenue: Room revenue × TRevPAR/RevPAR ratio
- GOP: Total revenue minus all operating expenses (per USALI structure)
- NOI: GOP minus FF&E reserve minus fixed charges
- Table: Base case / Upside / Downside model parameters in AED
- Insight: one-sentence summary
- Source: `STR Industry Data/`, `USALI Hotel Accounting Standards/`

### P7-2: Cash Flow and Returns
**Title**: Strong cash-on-cash returns supported by Disneyland Abu Dhabi upside
- 5–10 year DCF with projected RevPAR growth and margin assumptions
- Going-in cap rate on Year 1 NOI | Stabilised yield on Year 3–5 NOI
- IRR and equity multiple: Base / Upside (Disneyland) / Downside scenarios
- Sensitivity: occupancy ±5pp | ADR growth ±2% | exit cap ±50bps | CapEx ±25%
- Table: 10-year cash flow forecast in AED
- Insight: one-sentence summary

### P8-1: Investment Opportunity Analysis
**Title**: Three structural advantages create compelling entry point
- Theme park ecosystem: captive demand, park-stay bundle, Annual Pass
- Disneyland pipeline upside (occupancy and ADR impact) — read from `Future Reports/`; do not hardcode projections
- Supply discipline: Miral controls expansion — read from `Future Reports/`
- Table: Opportunity scoring matrix
- Insight: one-sentence summary

### P8-2: Risk Analysis and Mitigation
**Title**: Key risks are identifiable and manageable within Miral's ecosystem
- Event concentration risk (F1 and other anchor events) — quantify from `STR Industry Data/`; do not hardcode contribution %
- Seasonality: peak/shoulder/low periods — read from `DCT/` and `STR Industry Data/`
- Demand driver dependency: Miral attraction performance directly affects hotel demand
- Supply pipeline risk — read from `Future Reports/`
- Table: Risk register — ranked with probability / impact / mitigation
- Insight: one-sentence summary

### P9: Comprehensive Investment Recommendation
**Title**: [Hotel name] presents a [strong/moderate] investment case — [Go/No-Go]
- Overall verdict: go/no-go with key conditions
- Top 3 investment opportunity points with execution path
- Key risks and mitigation strategies
- Recommended entry timing and exit strategy
- All monetary figures in AED (USD conversion: AED 3.6725 = USD 1.00)
- Insight: forward-looking, actionable one-sentence summary

---

## Step 4 — Quality Verification

**Completeness check:**
- All pages P1–P9 generated with no missing sub-modules
- Tables, models, and parameters complete
- In-depth analysis on key decisions (opportunities, risks, strategies)

**Data annotation check:**
- `[source: filename]` tag at end of every page — trace to actual fetched filename
- All figures from PDFs or .xlsx confirmed against extracted content
- No fabricated data — use `≈` with estimation logic if actual data unavailable
- `[FETCH FAILED — verify manually]` flagged for any document that failed to load

**Format check:**
- All subheadings retained
- KPI formulas correct (RevPAR = Occupancy × ADR confirmed every period)
- Tables complete and consistent
- All figures in AED unless USD explicitly requested

**Financial model checks:**
- DCF terminal value ≤ 65–70% of total NPV
- NOI treats FF&E reserve below the line (per USALI convention)
- Cap rate = Year 1 NOI / Price (not EBITDA)
- Comp set matches chain scale and geography — never mix Yas Island with city hotels
- Miral-owned vs. third-party on Miral land clearly stated

---

## Step 5 — Generate HTML Display Page

After completing the P1–P9 report, generate a single HTML file containing
all pages — viewable in any browser and printable as PDF.

### HTML Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>[Hotel Name] — Miral Hotel Investment Analysis</title>
  <style>
    /* Main color: #1a3c5e (Miral navy) accent: #c8a96e (Miral gold) */
    /* Table gradient background, slide layout, print-ready CSS */
  </style>
</head>
<body>
  <div class="container">
    <!-- One <div class="slide"> per page P1–P9 -->
  </div>
</body>
</html>
```

### Required elements per page (slide)
- `<!-- PX: Page title -->` — HTML comment marking page number
- `<h1 class="slide-title">` — headline (15–20 words, opinion-style)
- `<div class="key-data">` — core KPIs (optional)
- `<div class="table-container"><table>` — data table (optional)
- `<div class="slide-content">` — body content (optional)
- `<div class="insight-box">` — insight summary (required)
- `<p class="data-source">` — data source citation with filenames (required)

### HTML characteristics
- **Single file**: all CSS embedded, no external dependencies
- **Shareable**: send via email or messaging apps
- **Printable**: print to PDF directly from browser
- **Cross-platform**: opens in any modern browser

---

## Quality Requirements

### Rules that must be followed
- **Relevance**: all content must relate to Miral hotel investment analysis
- **Format compliance**: strictly follow P1–P9 template — no deviations
- **Complete structure**: retain all subheadings, KPI formulas, and tables
- **Data integrity**: all data from fetched documents — no fabrication
- **Source tracing**: cite actual filename (not just folder) for every data point
- **Currency**: all figures in AED unless USD explicitly requested

### Data source priority
1. Fetched PDF/xlsx from GitHub knowledge base (highest priority)
2. Miral official press releases and annual reports
3. DCT Abu Dhabi official statistics
4. STR UAE / CBRE MENA / JLL MENA published reports
5. OTA platforms (Booking.com, Expedia) for rate benchmarking
6. Estimated with `≈` and stated logic (lowest priority)

### Time range
2022–2025 data; priority given to 2024 full-year figures where available.

---

## Usage Examples

### Example 1 — Single asset analysis
**Target hotel**: The WB Abu Dhabi
**Analysis type**: Acquisition underwriting
**Execution**:
- Fetch all folders (full IC memo)
- Extract text from PDFs; read Cluster STR .xlsx for comp set data
- Generate P1–P9 analysis focused on WB Abu Dhabi
- Annotate all data with source filenames
- Generate HTML report

### Example 2 — Benchmarking only
**Target hotel**: Crowne Plaza Yas Island
**Analysis type**: RevPAR benchmarking vs. comp set
**Execution**:
- Fetch `STR Industry Data/` (PDFs + `Cluster STR/` .xlsx only)
- Generate P4 and P5 only (performance + comp set analysis)
- Deliver KPI dashboard table with filename citations

### Example 3 — Full portfolio review
**Target**: All Miral-owned hotels (Hilton Yas Island, WB Abu Dhabi, DoubleTree)
**Analysis type**: Portfolio investment committee memo
**Execution**:
- Fetch all 5 folders
- Extract all PDFs and .xlsx
- Generate P1–P9 at portfolio level
- Annotate all sources with filenames
- Generate HTML display page

---

## Notes

- Fetch documents fresh every time — never rely on prior session memory
- Recursive discovery is required — subfolders exist (especially `STR Industry Data/Cluster STR/`)
- PDFs must be downloaded locally before text extraction — cannot stream binary from GitHub
- Excel files: read all sheets; STR cluster data typically spans multiple tabs by hotel/date
- Insight summaries must be forward-looking and actionable
- Flag all unverified figures with `[VERIFY]`
- If context limit is reached mid-analysis, prompt user:
  *"P1–P5 generated. Continuing with P6-1 through P9. Please confirm to proceed."*
