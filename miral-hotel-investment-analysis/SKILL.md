---
name: miral-hotel-investment-analysis
description: >
  Produces structured hotel investment analysis and reporting for Miral's hospitality
  portfolio across Yas Island and Saadiyat Island, Abu Dhabi, UAE. Use this skill
  whenever the user asks to analyze, evaluate, benchmark, underwrite, or report on
  any Miral hotel asset — including The WB Abu Dhabi, Hilton Yas Island, DoubleTree
  Yas Island, or any hotel operating within Miral's destination ecosystem. Also
  triggers for broader Yas Island or Saadiyat Island hospitality portfolio reviews,
  RevPAR benchmarking, ADR analysis, investment committee memos, acquisition
  feasibility, or cap rate / IRR modeling for UAE leisure-anchored hotels. Always
  use this skill when the user mentions Miral hotels, Yas Plaza Hotels, Yas Island
  hospitality, Saadiyat Island resorts, or UAE theme-park-adjacent hotel investment.
---

# Miral Hotel Investment Analysis

Structures hotel and hospitality investment analysis for Miral's portfolio on
Yas Island and Saadiyat Island, Abu Dhabi — with RevPAR, ADR, and operational
benchmarking calibrated to UAE market dynamics, Miral's destination model, and
Abu Dhabi's tourism growth strategy.

---

## Miral Portfolio Reference

### Miral-Owned Hotels (Hilton-Operated)
| Hotel | Brand | Stars | ~Rooms | Location |
|---|---|---|---|---|
| Hilton Abu Dhabi Yas Island | Hilton | 5★ | 545 | Yas Island |
| The WB Abu Dhabi | Curio Collection by Hilton | 5★ | ~294 | Yas Island |
| DoubleTree by Hilton Yas Island Residences | Hilton | 4★ | ~186 | Yas Island |

### Yas Plaza Hotels Cluster (IHG/Radisson-Operated, on Miral Land)
| Hotel | Brand | Stars | ~Rooms | Location |
|---|---|---|---|---|
| Crowne Plaza Yas Island | IHG | 4★ | 428 | Yas Island |
| Yas Plaza Marina | IHG | 4★ | ~234 | Yas Island |
| Yas Plaza Circuit | IHG | 4★ | ~234 | Yas Island |
| Yas Plaza Mangroves | IHG | 4★ | TBC | Yas Island |
| Staybridge Suites Yas Island | IHG | 4★ | — | Yas Island |
| Park Inn by Radisson Yas Island | Radisson | 3★ | 204 | Yas Island |

### Third-Party Hotels on Miral-Managed Destination
| Hotel | Brand | Stars | ~Rooms | Location |
|---|---|---|---|---|
| W Abu Dhabi – Yas Island | Marriott (W) | 5★ | 499 | Yas Island |
| Radisson Blu Hotel Yas Island | Radisson | 4★ | 397 | Yas Island |
| Yas Island Rotana | Rotana | 4★ | 308 | Yas Island |
| Centro Yas Island | Rotana | 3★ | 259 | Yas Island |
| Saadiyat Rotana Resort & Villas | Rotana | 5★ | — | Saadiyat Island |
| Park Hyatt Abu Dhabi | Hyatt | 5★ | — | Saadiyat Island |
| Rixos Premium Saadiyat Island | Rixos | 5★ | — | Saadiyat Island |
| St. Regis Saadiyat Island | Marriott | 5★ | — | Saadiyat Island |

**Total Yas Island inventory**: ~3,217 keys across 10 properties (2024)
**Expansion pipeline**: +~1,000 keys targeted over 2025–2030

---

## Miral Destination Context

### Yas Island Demand Drivers
- **Theme parks**: Ferrari World, Warner Bros. World, SeaWorld, Yas Waterworld
  — combined 38M+ visits in 2024 (10% YoY growth)
- **Upcoming**: Disneyland Abu Dhabi (7th Disney resort globally, announced May 2025),
  Harry Potter land at Warner Bros. World, Ferrari World record roller coaster
- **Events**: Formula 1 Abu Dhabi Grand Prix (Yas Marina Circuit), Etihad Arena
  (UAE's largest indoor arena — concerts, UFC, NBA, musicals)
- **Leisure**: Yas Links Golf Course (ranked top 34 globally), Yas Marina,
  Yas Bay Waterfront (20+ restaurants), Yas Mall, CLYMB Abu Dhabi
- **Miral's park-stay bundle**: Every hotel night = complimentary access to
  one Yas theme park. This is a core occupancy driver and rate justifier.

### Saadiyat Island Demand Drivers
- **Culture**: Louvre Abu Dhabi, teamLab Phenomena (opened April 2025),
  Natural History Museum Abu Dhabi (2025), Guggenheim Abu Dhabi (pipeline),
  Zayed National Museum (pipeline)
- **Leisure**: Saadiyat Beach, Saadiyat Beach Golf Club, luxury resort strip
- **Visitor profile**: Cultural tourism, luxury leisure, GCC weekend travellers,
  growing China (58% YoY growth 2024) and India (30% YoY) markets

### Abu Dhabi Tourism Macro
- **Strategy**: Tourism Strategy 2030 targets 39.3M visitors annually,
  AED 90B contribution to GDP, 178,000 new jobs
- **Regulator**: Department of Culture and Tourism Abu Dhabi (DCT Abu Dhabi)
- **Currency**: AED (UAE Dirham). Pegged at AED 3.6725 per USD.
- **Taxes & Fees**: UAE VAT 5%, DTCM municipality fee (typically 4–6% on room revenue),
  tourism dirham fee (AED 7–20/room/night depending on hotel category)
- **Seasonality**: Peak = Oct–Apr (cooler weather, events season, F1 in Nov).
  Shoulder = May, Sep. Low = Jun–Aug (extreme heat; partially offset by
  school holiday domestic GCC demand and Miral summer campaigns)

---

## When To Use

- Evaluating a Miral hotel or Yas/Saadiyat hotel as an acquisition or disposition target
- Benchmarking an existing Miral asset vs. comp set or STR UAE data
- Underwriting a hotel development, expansion, or repositioning within Miral's ecosystem
- Preparing investment committee memos or feasibility studies for UAE leisure-hotel assets
- Analyzing RevPAR, ADR, occupancy trends across the Miral portfolio
- Modeling IRR, cap rates, and returns for UAE theme-park-adjacent hospitality

---

## Inputs To Gather

- **Property profile**: Hotel name, brand/flag, operator, star rating, room count,
  location (Yas Island / Saadiyat Island / other), property type
  (full-service, select-service, branded residence, serviced apartment)
- **Operating data**: T12 and 3–5 year P&L, STR UAE report if available,
  monthly revenue segmentation (transient leisure, group, corporate, GCC domestic,
  international), theme park package revenue contribution
- **Market data**: Yas Island or Saadiyat Island comp set performance, new supply
  pipeline, Miral destination attendance data, F1/event calendar impact
- **Capital stack**: Acquisition price or book value, debt terms, FF&E reserve,
  PIP obligations, brand standard compliance costs in AED
- **Macro context**: DCT Abu Dhabi tourism stats, STR MENA/UAE data, CBRE MENA
  Hospitality Trends report, JLL MENA Hotel Investor Sentiment Survey
  [VERIFY against latest published editions]

---

## Workflow

### 1. Compute Core KPIs

- **RevPAR** = Occupancy × ADR. Compare to Yas Island / Saadiyat Island benchmarks:
  - Yas Island portfolio average: ~82% occupancy, peak 90% (Aug 2024)
  - ADR peak: AED 1,470 (The WB Abu Dhabi, Aug 2025)
  - Saadiyat Island: ~74% occupancy (2024), ADR ~AED 1,000 average
- **RevPAR Index (RGI)** vs. comp set: RGI > 100 = market outperformance
- **ADR growth vs. UAE CPI** — flag if ADR growth trails inflation 2+ years
- **Occupancy**: Stabilised vs. ramp-up. Note F1 weekend spike, summer trough,
  Ramadan pattern (leisure-heavy, F&B suppressed)
- **TRevPAR**: Total revenue per available room — critical for full-service and
  resort assets. Includes F&B, spa, theme park package uplift, resort fees
- **GOPPAR**: Gross operating profit per available room. Primary profitability
  metric. Compare to CBRE MENA chain-scale benchmarks [VERIFY latest edition]
- **Theme park attachment rate**: % of guests taking park-stay bundle.
  High attachment = rate integrity + occupancy driver unique to Miral assets.

### 2. Assess Revenue Segmentation & Rate Strategy

- Break revenue into:
  - **Leisure transient** (BAR, OTA, Miral.ae/direct, tour operators)
  - **GCC domestic** (Abu Dhabi residents, Dubai, KSA, Kuwait weekend travellers)
  - **International** (UK, India, China, Russia, Europe — verify current mix)
  - **Group & MICE** (corporate events, conferences, Etihad Arena overflow)
  - **Contract** (airline crew, government, long-stay)
- **OTA dependency**: OTA mix > 25–30% of transient signals rate integrity risk
  and commission drag. Miral's direct booking push (Miral Destinations portal,
  Yas Annual Pass) is a structural mitigant — quantify its share.
- **Event-driven demand**: F1 weekend, Etihad Arena concert series, public
  holidays. Model separately — these compress RevPAR index but spike ADR.
- **Yas Annual Pass impact**: Sold-out pass programme drives repeat visitation
  and hotel demand. Assess room night contribution and length of stay.

### 3. Analyse Operating Efficiency

- **Labor cost as % of revenue**: Benchmark — 30–35% full-service,
  22–28% select-service [VERIFY vs. current UAE/Abu Dhabi labor market rates]
- **Departmental margins**:
  - Rooms: 70–80% target
  - F&B: 25–35% target (note: Ramadan suppresses F&B revenue significantly)
  - Other operated departments (spa, parking, theme park packages)
- **FF&E reserve adequacy**: Industry standard 4% of gross revenue.
  Flag if actual spend or reserve < 3%.
- **PIP exposure**: Estimate cost per key for brand-mandated renovations (AED).
  Hilton, IHG, Marriott, Rotana, Radisson each have distinct PIP timelines and
  cost thresholds — verify against brand standards.
- **Theme park operational overlap**: Assess any shared-services arrangements
  between Miral hotel operations and theme park/destination management.
- **Sustainability operating costs**: Miral hotels have committed to eco-efficiency
  programmes (solar on Warner Bros. World, Hilton eco-initiatives). Note CapEx
  and OpEx implications for green certifications.

### 4. Model Investment Returns

- Build a 5–10 year DCF using:
  - Projected RevPAR growth (blend of Yas Island macro + Disneyland pipeline lift)
  - Margin expansion/compression assumptions
  - Terminal cap rate calibrated to UAE/GCC hospitality market
- **Going-in cap rate**: On Year 1 NOI after FF&E reserve
- **Stabilised yield**: On Year 3–5 NOI (post-ramp or post-renovation)
- **IRR and equity multiple**: Base, upside (Disneyland demand surge),
  downside (regional conflict, oil price shock, demand concentration) scenarios
- **Sensitivity matrix**: Occupancy (±5 pts), ADR growth (±1–2%), exit cap rate
  (±50 bps), CapEx overruns (±15–25%), AED/USD peg stability (note: peg is
  stable but model as fixed for conservatism)
- **Disneyland Abu Dhabi uplift scenario**: Model incremental RevPAR and occupancy
  impact from expected 20–32M+ annual Disney visitors on Yas Island hotel demand.
  Flag opening timeline risk [VERIFY current construction schedule].

### 5. Evaluate Market & Risk Factors

- **New supply as % of existing inventory**: Flag if Yas Island or Saadiyat Island
  pipeline exceeds 3–5% of current stock. Note the ~1,000 room Miral expansion plan.
- **Demand driver concentration**: Assess dependency on:
  - Single event (F1 weekend represents outsized RevPAR concentration risk)
  - Miral attraction attendance (if parks underperform, hotel demand weakens)
  - Theme park operational risk (closure, incident, brand damage)
- **Regulatory & tax risk**: DCT Abu Dhabi policy changes, municipality fee
  adjustments, UAE VAT rate changes, tourism levy revisions
- **Geopolitical risk**: UAE regional stability, GCC travel corridor dependency,
  Abu Dhabi vs. Dubai hotel competition dynamics
- **Management & franchise agreement terms**: Remaining term, termination
  provisions, performance tests, key money, brand fee structures
  (Hilton, IHG, Marriott, Rotana, Radisson fee tiers differ materially)
- **Miral master developer risk**: For third-party owned hotels on Miral land —
  assess ground lease terms, destination management fee structures, and
  dependency on Miral's broader investment in the island
- **Seasonality risk**: UAE summer (Jun–Aug) structural low season. Assess
  whether Miral summer activation programmes (kids campaigns, "Kids Go Free"
  offers) sufficiently mitigate trough occupancy.

---

## Output

Deliver a structured investment analysis containing:

### Executive Summary
Asset overview, investment thesis (2–3 sentences), go/no-go recommendation
with key conditions, and one-line Miral destination context (Yas vs. Saadiyat,
owned vs. third-party).

### KPI Dashboard
Table with Occupancy, ADR (AED), RevPAR (AED), TRevPAR, GOPPAR, GOP margin,
Theme Park Attachment Rate — actuals vs. Yas/Saadiyat Island benchmark vs. underwriting.

### Revenue & Expense Analysis
Segmentation breakdown (leisure, GCC domestic, international, group, contract),
margin benchmarking, labor and CapEx commentary, Miral park-stay bundle
contribution assessment.

### Financial Model Summary
Going-in cap rate, stabilised yield, IRR/equity multiple across base / Disneyland
upside / downside scenarios, sensitivity matrix in AED.

### Risk Register
Ranked list of material risks with mitigation strategies:
event concentration, demand driver dependency, supply pipeline, PIP cost,
AED-denominated rate risk, Miral master developer dependency, seasonality.

### Appendices
Comp set definition, STR UAE / CBRE MENA data sources, key assumptions table
(AED rates, UAE VAT, DTCM fees, FF&E %, terminal cap rate), Miral portfolio context.

---

## Quality Checks

- Confirm RevPAR = Occupancy × ADR across all periods
- Verify comp set uses same chain scale, geography (Yas vs. Saadiyat vs. Abu Dhabi city),
  and competitive positioning — do not mix full-service and select-service
- Ensure DCF terminal value does not exceed 65–70% of total value;
  if it does, stress-test terminal cap rate assumptions
- Check CapEx and PIP estimates are denominated in AED and tie to brand standards
  for the specific operator (Hilton ≠ IHG ≠ Rotana PIP requirements)
- Flag all data gaps with [VERIFY] — especially STR UAE data vintage,
  DCT Abu Dhabi stats recency, Disneyland opening timeline, and
  Miral expansion room count confirmations
- Confirm NOI calculation treats FF&E reserve as below-the-line for cap rate
  purposes (industry convention)
- All monetary figures must be in AED unless explicitly requested in USD
  (use AED 3.6725 = USD 1.00 for conversion)
- Note if analysis covers a Miral-owned asset vs. third-party asset on Miral land —
  risk profile, lease structure, and investment rationale differ materially

---

## Reference Documents — Auto-Discovered from GitHub at Runtime

Reference documents are stored in the Miral skills GitHub repository. The skill
**automatically discovers all available files** at runtime — no hardcoded filenames.
This means new documents added to the repo are picked up without any skill update.

### Repository Details
```
Owner : miralaipc
Repo  : skills
Branch: dev
Path  : miral-hotel-investment-analysis/documents
```

### Step 1 — Always Auto-Discover First

At the start of every analysis, call the GitHub Contents API to list all files
currently in the documents folder:

```
web_fetch("https://api.github.com/repos/miralaipc/skills/contents/miral-hotel-investment-analysis/documents?ref=dev")
```

This returns a JSON array. Each item has:
- `name`       — filename (e.g. `uae-market-benchmarks.md`)
- `download_url` — direct raw URL to fetch the file content

**Parse the response to get the full current file list.** Do not assume which files
exist — the folder may have grown since the skill was last updated.

### Step 2 — Select Relevant Documents

From the discovered file list, select which files to fetch based on the user's task.
Use the filename and any description hints to match relevance:

| If the task involves... | Likely relevant filenames contain... |
|------------------------|--------------------------------------|
| RevPAR, ADR, occupancy, seasonality, F1, supply | `benchmark`, `market`, `kpi`, `performance` |
| DCF, IRR, cap rate, NOI, CapEx, sensitivity, PIP | `financial`, `model`, `assumption`, `dcf` |
| Hotel profiles, comp sets, brand fees | `hotel`, `profile`, `comp`, `brand` |
| Full IC memo / complete analysis | fetch ALL discovered files |

If unsure, fetch all — it's better to have more context than to miss a document.

### Step 3 — Fetch File Contents

For each selected file, use its `download_url` from the Step 1 response:

```
web_fetch(<download_url from Contents API response>)
```

Raw URLs follow this pattern (but always prefer the `download_url` from the API):
```
https://raw.githubusercontent.com/miralaipc/skills/refs/heads/dev/miral-hotel-investment-analysis/documents/<filename>
```

### Step 4 — Use the Content

Read and incorporate the fetched document content into your analysis.
Treat all fetched content as authoritative — it is the single source of truth
for Miral-specific benchmarks, assumptions, and hotel profiles.

### Fetch Error Handling

| Scenario | Action |
|----------|--------|
| Contents API returns empty array | Warn user: "No documents found in GitHub repo. Check repo path and branch." |
| Contents API fails (network/403) | Warn user, proceed with built-in SKILL.md knowledge only, flag all figures with `[VERIFY]` |
| Individual file fetch fails | Skip that file, note it, continue with others |
| File is not markdown (e.g. `.xlsx`, `.pdf`) | Skip — only process `.md` and `.txt` files |

Always tell the user how many documents were discovered and which ones were loaded,
e.g.: *"Found 5 documents in the repository. Loaded 2 relevant to this analysis:
`uae-market-benchmarks.md` and `financial-model-assumptions.md`."*

---

## Key Data Sources (UAE/Miral-Specific)

- **STR UAE / STR MENA**: Comp set benchmarking, chain-scale RevPAR indices
- **CBRE MENA Hospitality Trends**: Annual chain-scale benchmarks, GOP margins
- **JLL MENA Hotel Investor Sentiment Survey**: Cap rate, transaction data
- **DCT Abu Dhabi**: Official Yas Island and Saadiyat Island visitor statistics
- **Miral annual reports / press releases**: Attendance, occupancy, ADR disclosures
- **DTCM (Dubai Tourism)**: Broader UAE market context
- **Knight Frank MENA Hospitality Report**: Investment trends, pipeline data
- **Booking.com / Expedia / OTA Insight**: Rate parity and OTA mix benchmarking
  [All sources: VERIFY recency before citing in final output]
