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
on real-time data fetched from the Miral GitHub knowledge base.

The analysis is executed in two steps:
- **Step 1**: Generate a detailed investment analysis report (P1–P9, 19 pages total)
- **Step 2**: Generate an HTML display page (viewable in browser, printable as PDF)

---

## Task Objectives

This skill generates professional hotel investment analysis reports for Miral hotels.

Capabilities include:
- Automatically select the correct hotel profile and comp set based on the target hotel
- Fetch latest market data, benchmarks, and financial assumptions from GitHub knowledge base
- Generate complete analysis content following the P1–P9 template structure (19 pages)
- Provide KPI benchmarks across 5 key indices: occupancy, ADR, RevPAR, GOPPAR, GOP margin
- Provide detailed investment models (revenue, cost, cap rate, IRR, payback period)
- Provide data source annotations and investment recommendations
- Generate HTML display page (viewable in browser, printable as PDF)

**Trigger condition**: User provides a Miral hotel name and/or analysis type

---

## Role Positioning

### Data Retrieval Role
Fetch from the Miral GitHub knowledge base (private repo — PAT required):
- UAE and Abu Dhabi market benchmarks (STR UAE, CBRE MENA, DCT Abu Dhabi)
- Miral hotel financial model assumptions (cap rates, IRR, CapEx, DCF)
- Miral hotel profiles and comp set definitions

### Miral Hotel Investment Consultant Role
- Output professional analysis based on template structure
- Generate headline and insight summary for each page
- Provide investment potential assessment and risk recommendations

---

## Step 0 — Fetch Knowledge Base from GitHub (Always Do First)

Before any analysis, read the PAT from `~/.claude/CLAUDE.md` and fetch
reference documents from the Miral private GitHub repository.

### Read PAT
```bash
cat ~/.claude/CLAUDE.md
# Extract value after "GITHUB_PAT: "
```

### Repository Details
```
Owner  : miralaipc
Repo   : skills
Branch : main
Path   : miral-hotel-investment-analysis/documents
```

### Step 0a — Discover all documents
```
web_fetch(
  url     = "https://api.github.com/repos/miralaipc/skills/contents/miral-hotel-investment-analysis/documents?ref=main",
  headers = {
    "Authorization": "Bearer <PAT from CLAUDE.md>",
    "Accept":        "application/vnd.github+json"
  }
)
```
Parse the JSON array. Each item has `name` and `download_url`.
**Never hardcode filenames** — discover dynamically so new documents are
picked up automatically without updating this skill.

### Step 0b — Select relevant documents

| Task involves | Fetch files whose names contain |
|---|---|
| Occupancy, ADR, RevPAR, seasonality, F1, benchmarks | `benchmark`, `market`, `kpi`, `performance` |
| DCF, IRR, cap rate, NOI, CapEx, sensitivity, PIP | `financial`, `model`, `assumption`, `dcf` |
| Hotel profiles, comp sets, brand fees | `hotel`, `profile`, `comp`, `brand` |
| Full investment analysis or IC memo | fetch **all** files |

### Step 0c — Fetch each file
```
web_fetch(
  url     = "<download_url from Step 0a>",
  headers = {
    "Authorization": "Bearer <PAT from CLAUDE.md>",
    "Accept":        "application/vnd.github.raw"
  }
)
```

### Step 0d — Confirm to user
> *"Fetched 3 documents from GitHub: `uae-market-benchmarks.md`,
> `financial-model-assumptions.md`, `hotel-profiles-comp-sets.md`.
> Proceeding with analysis."*

### Error handling

| Scenario | Action |
|---|---|
| PAT not found in CLAUDE.md | Ask user to add: `GITHUB_PAT: ghp_xxx` to `~/.claude/CLAUDE.md` |
| 401 Unauthorized | PAT expired — regenerate at github.com/settings/tokens |
| 404 Not Found | Check repo path and branch name |
| Fetch fails | Proceed with built-in knowledge; flag all figures `[VERIFY]` |

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

### Miral-Owned Hotels (Hilton-Operated)
| Hotel | Brand | Stars | Rooms |
|---|---|---|---|
| Hilton Abu Dhabi Yas Island | Hilton | 5★ | 545 |
| The WB Abu Dhabi | Curio Collection by Hilton | 5★ | ~294 |
| DoubleTree by Hilton Yas Island Residences | Hilton | 4★ | ~186 |

### Yas Plaza Hotels (on Miral Land)
| Hotel | Brand | Stars | Rooms |
|---|---|---|---|
| Crowne Plaza Yas Island | IHG | 4★ | 428 |
| Yas Plaza Marina | IHG | 4★ | ~234 |
| Yas Plaza Circuit | IHG | 4★ | ~234 |
| Yas Plaza Mangroves | IHG | 4★ | TBC |
| Staybridge Suites Yas Island | IHG | 4★ | — |
| Park Inn by Radisson Yas Island | Radisson | 3★ | 204 |

### Third-Party Hotels on Miral-Managed Destination
| Hotel | Brand | Stars | Rooms |
|---|---|---|---|
| W Abu Dhabi – Yas Island | Marriott (W) | 5★ | 499 |
| Radisson Blu Hotel Yas Island | Radisson | 4★ | 397 |
| Yas Island Rotana | Rotana | 4★ | 308 |
| Centro Yas Island | Rotana | 3★ | 259 |

**Total Yas Island**: ~3,217 keys / 10 properties (2024)
**Pipeline**: +~1,000 keys planned 2025–2030

---

## Execution Process

### Step 1 — Identify Hotel and Select Profile

- Confirm target hotel name and analysis type from user
- Identify hotel category: Miral-owned / Yas Plaza cluster / Third-party on Miral land
- Load hotel profile and recommended comp set from `hotel-profiles-comp-sets.md`
- Load market benchmarks from `uae-market-benchmarks.md`
- Load financial assumptions from `financial-model-assumptions.md`

### Step 2 — Data Collection and Annotation

**Hotel KPI data:**
- Occupancy, ADR, RevPAR — from fetched benchmarks or user-provided P&L
- GOPPAR, GOP margin — from fetched financial assumptions
- Theme park attachment rate — unique to Miral assets

**Market data:**
- Yas Island / Saadiyat Island comp set performance
- New supply pipeline (current ~3,217 keys + ~1,000 planned)
- Key demand drivers: F1 Grand Prix, Etihad Arena events, Disneyland Abu Dhabi pipeline
- Seasonality: Peak Oct–Apr | Shoulder May, Sep | Low Jun–Aug

**Financial data:**
- UAE VAT: 5% | DTCM municipality fee: 4–6% of room revenue
- AED pegged at 3.6725 per USD
- Cap rates, IRR ranges, DCF assumptions — from `financial-model-assumptions.md`

**Data annotation**: mark all figures with `[source]` at end of each page.
Missing data: use `≈` with estimation logic clearly stated.

### Step 3 — Generate Analysis Content (P1–P9)

**First batch — P1 to P5:**
Follow template structure strictly. Retain all subheadings and table structures.
Generate a headline and insight summary for each page.

**Second batch — P6 to P9 (if needed):**
P6-1, P6-2 | P7-1, P7-2 | P8-1, P8-2 | P9

**Segmented generation strategy:**
If context limit is reached, prompt user:
*"P1–P5 analysis generated. Follow-up plan: continue with P6-1, P6-2, P7-1,
P7-2, P8-1, P8-2, P9. Please copy this plan to trigger continuation."*

---

## Report Template (P1–P9)

### P1: Abu Dhabi & Yas Island Macro Overview
**Title**: Steady tourism growth creates strong foundation for Yas Island hotels
- GDP growth, Abu Dhabi Tourism Strategy 2030, visitor numbers
- Yas Island: 38M+ visits 2024 (+10% YoY) | Saadiyat Island: +10% YoY
- Table: Key macro indicators with YoY growth
- Insight: one-sentence summary
- Source: DCT Abu Dhabi, Miral press releases

### P2: Demand Drivers Analysis
**Title**: Theme park ecosystem and events calendar drive year-round hotel demand
- Theme parks: Ferrari World, Warner Bros. World, SeaWorld, Yas Waterworld
- Events: F1 Grand Prix (Nov), Etihad Arena concerts, UFC, NBA
- Pipeline: Disneyland Abu Dhabi (7th Disney resort, announced May 2025)
- Park-stay bundle: 1 night = 1 complimentary park entry — unique demand driver
- Table: Annual events calendar with occupancy/ADR impact
- Insight: one-sentence summary
- Source: Miral, DCT Abu Dhabi, Formula 1

### P3: Hotel Market Supply Analysis
**Title**: Controlled supply with strong demand creates compelling investment case
- Total inventory: ~3,217 keys / 10 properties on Yas Island (2024)
- Grade distribution: 5★ / 4★ / 3★ / serviced apartments
- Pipeline: +~1,000 keys targeted 2025–2030 (Miral-controlled expansion)
- Table: Hotel inventory by brand, stars, rooms, category
- Insight: one-sentence summary
- Source: Miral press releases, STR UAE

### P4: Hotel Performance Benchmarks
**Title**: Yas Island hotels outperform Abu Dhabi market on all key KPIs
- Yas Island 2024: 82% occupancy (peak 90% Aug), ADR peak AED 1,470 (WB Hotel)
- Saadiyat Island 2024: 74% occupancy, ADR ~AED 1,000
- Abu Dhabi market: RevPAR +26% YoY (CBRE H2 2025)
- Table: Occupancy / ADR / RevPAR / GOPPAR / GOP margin — actuals vs. benchmarks
- Insight: one-sentence summary
- Source: Miral, CBRE MENA, STR UAE, DCT Abu Dhabi

### P5: Comp Set and Competitive Positioning
**Title**: Subject hotel positioned within a clearly defined competitive set
- Comp set definition for target hotel (from hotel-profiles-comp-sets.md)
- RevPAR Index (RGI) vs. comp set — RGI > 100 = outperformance
- OTA dependency: flag if > 25–30% of transient revenue
- Table: Subject hotel vs. comp set — Occupancy / ADR / RevPAR / RGI
- Insight: one-sentence summary
- Source: STR UAE, OTA platforms

### P6-1: Revenue Segmentation Analysis
**Title**: Diversified revenue base with theme park bundle as structural advantage
- Segments: leisure transient / GCC domestic / international / group & MICE / contract
- GCC domestic: Abu Dhabi residents, Dubai, KSA, Kuwait weekend travellers
- International growth: China +58% YoY, India +30% YoY, UK +11% YoY (2024)
- Table: Revenue segmentation breakdown with % contribution
- Insight: one-sentence summary

### P6-2: Operating Efficiency Analysis
**Title**: Labour and FF&E benchmarks reveal operational improvement opportunities
- Labour: 30–35% full-service / 22–28% select-service [VERIFY vs. UAE market]
- Departmental margins: Rooms 70–80% / F&B 25–35% / Spa 30–42%
- FF&E reserve: flag if below 3% of gross revenue (standard = 4%)
- PIP exposure: AED per key by brand (Hilton ≠ IHG ≠ Rotana ≠ Radisson)
- Table: Operating cost benchmarks vs. actuals
- Insight: one-sentence summary

### P7-1: Investment Model — Parameters
**Title**: Conservative assumptions anchored to verified Yas Island benchmarks
- Room revenue: Available rooms × 365 × Occupancy × ADR
- Total revenue: Room revenue × TRevPAR/RevPAR ratio
- GOP: Total revenue minus all operating expenses
- NOI: GOP minus FF&E reserve minus fixed charges
- Table: Base case / Upside / Downside model parameters in AED
- Insight: one-sentence summary

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
- Disneyland pipeline: projected +5–8pp occupancy, +10–20% ADR post-opening
- Supply discipline: Miral controls expansion — no disruptive third-party supply
- Table: Opportunity scoring matrix
- Insight: one-sentence summary

### P8-2: Risk Analysis and Mitigation
**Title**: Key risks are identifiable and manageable within Miral's ecosystem
- Event concentration: F1 weekend = ~8–12% of annual RevPAR
- Seasonality: Jun–Aug structural low (mitigated by school holiday theme park demand)
- Demand driver dependency: Miral attraction performance directly affects hotel demand
- Supply pipeline: +1,000 keys may pressure occupancy in mid-term
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
- `[source]` tag at end of every page
- All figures traced to STR UAE, CBRE MENA, DCT Abu Dhabi, or Miral disclosures
- No fabricated data — use `≈` with estimation logic if actual data unavailable

**Format check:**
- All subheadings retained
- KPI formulas correct (RevPAR = Occupancy × ADR confirmed every period)
- Tables complete and consistent
- All figures in AED unless USD explicitly requested

**Financial model checks:**
- DCF terminal value ≤ 65–70% of total NPV
- NOI treats FF&E reserve below the line (industry convention)
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
- `<p class="data-source">` — data source citation (required)

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
- **Data integrity**: all data sourced from verified references — no fabrication
- **Currency**: all figures in AED unless USD explicitly requested

### Data source priority
1. Fetched from GitHub knowledge base (highest priority)
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
- Fetch hotel profile and comp set from GitHub
- Load Yas Island benchmarks and financial assumptions
- Generate P1–P9 analysis focused on WB Abu Dhabi
- Annotate all data sources
- Generate HTML report

### Example 2 — Benchmarking only
**Target hotel**: Crowne Plaza Yas Island
**Analysis type**: RevPAR benchmarking vs. comp set
**Execution**:
- Fetch `uae-market-benchmarks.md` and `hotel-profiles-comp-sets.md`
- Generate P4 and P5 only (performance + comp set analysis)
- Deliver KPI dashboard table

### Example 3 — Full portfolio review
**Target**: All Miral-owned hotels (Hilton Yas Island, WB Abu Dhabi, DoubleTree)
**Analysis type**: Portfolio investment committee memo
**Execution**:
- Fetch all 3 GitHub documents
- Generate P1–P9 at portfolio level
- Annotate all sources
- Generate HTML display page

---

## Notes

- Read GitHub documents only when needed — keep context concise
- Always fetch fresh from GitHub — never rely on cached or built-in knowledge
- Strictly follow P1–P9 template structure and quality requirements
- Maintain logical consistency when generating in segments
- Data annotations must be accurate — professionalism depends on source quality
- HTML output should highlight key data, simplify body text, unify style
- Insight summaries must be forward-looking and actionable
- Flag all unverified figures with `[VERIFY]`
