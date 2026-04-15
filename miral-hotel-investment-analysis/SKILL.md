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
for Miral's hotel portfolio on Yas Island and Saadiyat Island, Abu Dhabi.

A GitHub Actions pipeline pre-extracts all source PDFs and xlsx files into a
lightweight `knowledge-base/` of markdown files. Claude reads only those files —
no PDF parsing, no slow downloads, no guessing.

---

## ⛔ STRICT GROUNDING RULES — READ BEFORE ANYTHING ELSE

These rules are mandatory and override all other instructions:

1. **Only use the knowledge base.** Every factual claim — hotel names, room
   counts, occupancy rates, ADR, RevPAR, brand fees, pipeline figures, market
   stats — must come verbatim from the loaded knowledge base files. No exceptions.

2. **No web search.** Do not search the web for any data, even if the knowledge
   base appears incomplete. Web data is unverified and may conflict with Miral's
   internal documents.

3. **No training knowledge for facts.** Do not use anything you know about Abu
   Dhabi hotels, STR benchmarks, or Miral from your training data. Your training
   data may be outdated or incorrect for this context.

4. **If it's not in the knowledge base, say so.** If a figure or fact cannot be
   found in the loaded files, write: `[NOT IN KNOWLEDGE BASE — data not available]`
   Do not estimate, do not infer, do not fill the gap.

5. **Every number needs a citation.** Format: `[source: filename.md]` immediately
   after every figure. If you cannot provide a citation, do not include the figure.

6. **Respect extraction quality flags.** If a file is marked `⚠ OCR` in the
   knowledge base, add `[OCR — verify against original]` next to every figure
   drawn from it. If marked `❌ FAILED`, do not cite any data from that file.

7. **Only permitted constants (no citation needed):**
   - UAE VAT: 5%
   - DTCM municipality fee: 4–6% of room revenue
   - AED/USD peg: 3.6725
   These are fixed regulatory/monetary facts, not market data.

**Violation of these rules produces a report that cannot be trusted or presented
to an investment committee. When in doubt, write `[NOT IN KNOWLEDGE BASE]`.**

---

## Repository Structure

```
miral-hotel-investment-analysis/
│
├── documents/              ← source PDFs and xlsx — NEVER read directly by Claude
│   ├── Brands/
│   ├── DCT/
│   ├── Future Reports/
│   ├── STR Industry Data/
│   │   └── Cluster STR/   ← .xlsx files
│   └── USALI Hotel Accounting Standards/
│
├── knowledge-base/         ← Claude reads ONLY these files
│   ├── _index.md           ← status, accuracy flags, last updated
│   ├── brands.md
│   ├── dct.md
│   ├── str-industry-data.md
│   ├── str-cluster-data.md
│   ├── future-reports.md
│   └── usali-standards.md
│
└── tools/
    └── extract.py          ← run by GitHub Actions only, never by Claude
```

**Knowledge base auto-updates** whenever any file under `documents/` is pushed
to main. Claude never runs `extract.py`.

---

## Step 0 — Load Knowledge Base (Always Do First)

### Read PAT

```bash
cat ~/.claude/CLAUDE.md
# Extract the value after "GITHUB_PAT: "
```

### Step 0a — Fetch Index

```python
import requests

PAT = "<from CLAUDE.md>"
RAW = "https://raw.githubusercontent.com/miralaipc/skills/main/miral-hotel-investment-analysis/knowledge-base"
HEADERS = {"Authorization": f"Bearer {PAT}"}

index = requests.get(f"{RAW}/_index.md", headers=HEADERS, timeout=15)
index.raise_for_status()
print(index.text)
```

Read the index carefully:
- Note the **last updated** date for each file
- Note any files marked `⚠ warnings` — apply OCR caution to those
- Note any files marked `❌ FAILED` — do not cite data from those

If `_index.md` returns 404: *"Knowledge base not found. Please trigger the
GitHub Action manually from the Actions tab, or push any file to `documents/`."*

### Step 0b — Select Files for This Query

| Task | Load |
|---|---|
| Occupancy, ADR, RevPAR, comp set | `str-industry-data.md`, `str-cluster-data.md` |
| Tourism stats, demand drivers, seasonality | `dct.md` |
| Brand fees, PIP, comp set definition | `brands.md` |
| GOP, departmental margins, P&L structure | `usali-standards.md` |
| Pipeline, future supply | `future-reports.md` |
| Full analysis or IC memo | **all 6 files** |

### Step 0c — Fetch Files

```python
FILES = {
    "brands":      "brands.md",
    "dct":         "dct.md",
    "str":         "str-industry-data.md",
    "str_cluster": "str-cluster-data.md",
    "future":      "future-reports.md",
    "usali":       "usali-standards.md",
}

knowledge = {}
for key, fname in FILES.items():
    r = requests.get(f"{RAW}/{fname}", headers=HEADERS, timeout=15)
    r.raise_for_status()
    knowledge[key] = r.text
```

### Step 0d — Confirm Before Proceeding

Tell the user exactly what was loaded and flag any issues:

> *"Knowledge base loaded: [list files]. Last updated: [date from index].
> ⚠ Note: [filename] used OCR — figures will be flagged for verification.
> Proceeding with analysis using knowledge base only."*

### Error Handling

| Scenario | Action |
|---|---|
| PAT missing from CLAUDE.md | Ask user: add `GITHUB_PAT: ghp_xxx` to `~/.claude/CLAUDE.md` |
| 401 Unauthorized | PAT expired — regenerate at github.com/settings/tokens (`repo` scope) |
| `_index.md` 404 | Knowledge base not yet built — ask user to trigger GitHub Action |
| Individual file 404 | Source folder is empty — note it, continue without that file |
| File marked `⚠ OCR` | Load file, add `[OCR — verify]` to all figures from it |
| File marked `❌ FAILED` | Do not load or cite — tell user this folder needs manual review |

---

## Step 1 — Identify Hotel and Build Portfolio Context

- Confirm target hotel name and analysis type from user
- Search `brands.md` for the hotel entry — extract brand, operator, room count,
  ownership category, comp set definition from the document text
- If hotel is not found in `brands.md`: write `[NOT IN KNOWLEDGE BASE]` and ask
  user to verify the hotel name or update the documents

---

## Step 2 — Data Collection Protocol

Before writing any analysis page, locate the specific passage in the knowledge
base that supports each figure. If you cannot find it, write `[NOT IN KNOWLEDGE BASE]`.

| Data needed | Source file | If not found |
|---|---|---|
| Hotel KPIs (Occ, ADR, RevPAR, GOPPAR) | `str-industry-data.md`, `str-cluster-data.md` | `[NOT IN KNOWLEDGE BASE]` |
| Tourism, visitor numbers, demand | `dct.md` | `[NOT IN KNOWLEDGE BASE]` |
| Departmental margins, P&L structure | `usali-standards.md` | `[NOT IN KNOWLEDGE BASE]` |
| Brand fees, PIP per key, comp set | `brands.md` | `[NOT IN KNOWLEDGE BASE]` |
| Supply pipeline, future scenarios | `future-reports.md` | `[NOT IN KNOWLEDGE BASE]` |

---

## Report Template (P1–P9)

Each page must follow this pattern:
- **Headline**: opinion-style, 15–20 words
- **Body**: figures from knowledge base only, each tagged `[source: filename.md]`
- **Insight box**: one forward-looking sentence grounded in the loaded data
- **Data source line**: list exact filenames used on this page

---

### P1: Abu Dhabi & Yas Island Macro Overview
Draw GDP, tourism strategy, visitor figures from `dct.md`.
If `dct.md` is empty or failed: mark entire page `[NOT IN KNOWLEDGE BASE — DCT documents unavailable]`.

### P2: Demand Drivers Analysis
Draw theme park, events, pipeline data from `dct.md` and `future-reports.md`.

### P3: Hotel Market Supply Analysis
Draw total inventory, grade mix, pipeline keys from `str-industry-data.md`
and `future-reports.md`. Build supply table from document content — do not
construct it from memory.

### P4: Hotel Performance Benchmarks
Draw all KPI figures from `str-industry-data.md` and `str-cluster-data.md`.
Table columns: Occupancy / ADR / RevPAR / GOPPAR / GOP Margin.
Every cell must have `[source: filename.md]` or `[NOT IN KNOWLEDGE BASE]`.

### P5: Comp Set and Competitive Positioning
Draw comp set definition from `brands.md`. Draw RGI and performance
comparison from `str-cluster-data.md`. If comp set not defined in `brands.md`:
write `[NOT IN KNOWLEDGE BASE — comp set not defined for this hotel]`.

### P6-1: Revenue Segmentation Analysis
Draw segment breakdown and source market data from `dct.md`.

### P6-2: Operating Efficiency Analysis
Draw departmental benchmarks from `usali-standards.md`.
Draw PIP per key and FF&E reserve standards from `brands.md`.

### P7-1: Investment Model — Parameters
Draw RevPAR/ADR inputs from `str-cluster-data.md`.
Use USALI P&L structure from `usali-standards.md` for revenue → GOP → NOI build.
Table: Base / Upside / Downside — all cells sourced or marked `[NOT IN KNOWLEDGE BASE]`.

### P7-2: Cash Flow and Returns
Build 5–10 year DCF using only figures drawn from knowledge base in P7-1.
Do not apply assumed growth rates — use only rates found in the documents.
If growth assumptions are not in the knowledge base, state the assumption
explicitly and mark it `[ASSUMPTION — not in knowledge base]`.

### P8-1: Investment Opportunity Analysis
Draw opportunity framing from `future-reports.md` and `dct.md`.

### P8-2: Risk Analysis and Mitigation
Draw event concentration, seasonality risk, supply risk from
`str-cluster-data.md` and `future-reports.md`.

### P9: Investment Recommendation
Synthesise from knowledge base findings only. Do not introduce any new
figures or claims not already cited in P1–P8. State the basis for the
recommendation in terms of which knowledge base files support it.

---

## Step 4 — Quality Check Before Delivering

Run through this checklist before presenting output to the user:

- [ ] Every figure has `[source: filename.md]` or `[NOT IN KNOWLEDGE BASE]`
- [ ] No figure introduced in P9 that wasn't cited in P1–P8
- [ ] No web search was used at any point
- [ ] No training knowledge used for any market figure or hotel fact
- [ ] OCR-sourced figures carry `[OCR — verify]`
- [ ] Failed files are not cited anywhere
- [ ] KPI formula check: RevPAR = Occupancy × ADR for every row
- [ ] All figures in AED unless user explicitly requested USD

If any check fails, fix it before delivering. Do not present a report with
uncited figures to the user.

---

## Step 5 — HTML Display Page

Single file, all CSS embedded, print-ready.
Colors: `#1a3c5e` (Miral navy), `#c8a96e` (Miral gold).
One `<div class="slide">` per page P1–P9.

Each slide requires:
- `<h1 class="slide-title">` — headline
- `<div class="insight-box">` — insight
- `<p class="data-source">` — list exact filenames used on this slide
- `[NOT IN KNOWLEDGE BASE]` cells rendered in amber to make gaps visible

---

## Notes

- **Never run `extract.py`** — GitHub Actions handles this automatically
- **Never read from `documents/`** — always read from `knowledge-base/`
- If context limit reached: *"P1–P5 done. Continuing with P6–P9 — confirm to proceed."*
- If knowledge base appears stale (>7 days): suggest user push a file to trigger re-extraction
