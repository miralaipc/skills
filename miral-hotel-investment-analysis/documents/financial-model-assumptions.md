# Financial Model Assumptions & DCF Template — Miral Hotels

> Use this reference when building investment models for Miral portfolio hotels
> All monetary figures in AED unless noted. AED 3.6725 = USD 1.00 (fixed peg)
> [VERIFY all assumptions against current market data before finalising model]

---

## Table of Contents
1. Standard Model Assumptions
2. Miral-Specific Adjustments
3. DCF Structure Template
4. Sensitivity Matrix Framework
5. Cap Rate Reference — UAE/GCC Hospitality
6. Scenario Definitions (Base / Upside / Downside)
7. Key Ratios & Quality Checks

---

## 1. Standard Model Assumptions

### Revenue Assumptions
| Parameter | Conservative | Base Case | Optimistic | Notes |
|-----------|-------------|-----------|------------|-------|
| RevPAR growth Yr 1–3 | 3% | 5–6% | 8–10% | Post-stabilisation |
| RevPAR growth Yr 4–10 | 2% | 3–4% | 5–6% | Mature phase |
| ADR growth (annual) | 2–3% | 3–4% | 5–7% | Vs. UAE CPI ~3–4% |
| Occupancy stabilised | 75% | 80–82% | 85–88% | Yas Island target |
| TRevPAR / RevPAR ratio | 1.15x | 1.25x | 1.35x | Higher for full-service |
| OTA commission | 18–20% | 15–18% | 12–15% | Of OTA-generated revenue |
| OTA share of transient | 22% | 18% | 14% | Miral direct booking push |

### Operating Cost Assumptions
| Cost Line | % of Revenue | Notes |
|-----------|-------------|-------|
| Rooms labour | 12–14% | Select-service; 15–18% full-service |
| F&B labour | 28–32% | Higher in UAE due to staffing model |
| Total labour | 28–35% | Full-service; 22–28% select-service |
| FF&E reserve | 4.0% | Industry standard; minimum 3% |
| Management fee | 2–3% of gross revenue | Base; + incentive fee on GOP |
| Franchise / brand fee | 5–7% of room revenue | Varies by brand |
| Insurance | 0.5–1.0% | UAE property insurance |
| Property tax / municipality | 4–6% of room revenue | DTCM municipality fee |
| UAE VAT | 5% | Applied to room revenue |
| Tourism dirham | AED 7–20/room/night | By hotel category |

### CapEx Assumptions
| Item | AED per Key | Frequency | Notes |
|------|------------|-----------|-------|
| FF&E reserve (annual) | AED 18,000–45,000 | Annual | 4% of gross revenue |
| Soft renovation (refresh) | AED 35,000–60,000 | Every 5–7 years | Carpets, soft furnishings |
| Hard PIP (brand standard) | AED 90,000–200,000+ | Every 10–15 years | Full room gut renovation |
| Public area renovation | AED 5,000–15,000/key | Every 7–10 years | Lobby, F&B, pool |
| MEP / infrastructure | AED 10,000–25,000/key | Ad hoc / lifecycle | HVAC, elevators |

**Miral-specific PIP note**: Hilton (WB, Hilton Yas, DoubleTree), IHG (Crowne Plaza, Yas Plaza),
Marriott (W), Rotana (Yas Rotana, Centro), Radisson (Blu, Park Inn) each have distinct brand
standard cycles and cost thresholds. Always verify with operator prior to finalising PIP budget.

---

## 2. Miral-Specific Adjustments

### Theme Park Attachment Rate
| Hotel Category | Attachment Rate | Impact on ADR | Notes |
|----------------|----------------|--------------|-------|
| 5★ Miral-owned (WB, Hilton) | 65–80% | +AED 80–150/night effective | Park value bundled |
| 4★ Yas Plaza cluster | 70–85% | +AED 60–100/night effective | Core Yas proposition |
| 3★ / select-service | 80–90% | +AED 40–70/night effective | Budget travellers value |

**How to model**: Use RevPAR inclusive of park-stay value vs. market comps that exclude it.
Clearly separate room-only ADR from effective ADR (including park access value) in the model.
The park-stay bundle is a structural rate floor — it makes deep discounting less necessary.

### Disneyland Abu Dhabi Uplift Scenario
Apply to Base + Upside scenarios once opening timeline is confirmed:
- Phase 1 (Opening year): Occupancy +5–8pp on Yas Island; ADR +10–20%
- Phase 2 (Stabilised, 3+ years post-opening): Occupancy +3–5pp sustained; ADR +5–10%
- Assumption: Disney projects 20–32M first-year visitors; even modest hotel conversion
  drives significant room night demand across entire Yas Island portfolio
- [VERIFY opening timeline before applying]

### Miral Destination Management Premium
Hotels on Miral-managed destinations (Yas Island, Saadiyat Island) command:
- 15–25% RevPAR premium vs. comparable Abu Dhabi city hotels (source: Miral data)
- Lower marketing cost per booking (Miral Destinations portal centralised distribution)
- Higher repeat visitation through Yas Annual Pass (sold out 2025)

### F1 Grand Prix Model
- Model separately as a 4-night event (Thu–Sun)
- ADR premium: 3–5x BAR rate on race weekend
- Occupancy: 95–100% across Yas Island properties
- ADR premium accounts for ~8–12% of annual RevPAR for Yas Island hotels
- Apply in November in 5-year model (contractual through 2030 at minimum)

---

## 3. DCF Structure Template

### Year-by-Year Build (10-Year Model)

**Revenues:**
```
Room Revenue = Available Rooms × 365 × Occupancy × ADR
Other Revenue = Room Revenue × (TRevPAR/RevPAR ratio - 1)
Total Revenue = Room Revenue + Other Revenue
```

**Operating Expenses:**
```
Rooms Expense = Room Revenue × Rooms Dept Cost %
F&B Expense = F&B Revenue × F&B Dept Cost %
Other Dept Expenses = Other Revenue × Other Dept Cost %
Undistributed Expenses = Total Revenue × Undistributed %
  [Admin & General: 8–10%, Sales & Marketing: 5–7%, Maintenance: 4–6%, Utilities: 3–5%]
Management Fee = Total Revenue × 2–3%
GOP = Total Revenue - All Operating Expenses
FF&E Reserve = Total Revenue × 4%
NOI (for cap rate) = GOP - FF&E Reserve - Fixed Charges
  [Fixed Charges: Insurance, Property Tax, Ground Lease if applicable]
```

**Valuation:**
```
Going-in Cap Rate = Year 1 NOI / Acquisition Price
Stabilised Yield = Year 3–5 NOI / Acquisition Price
Terminal Value = Year 10 NOI / Terminal Cap Rate
NPV / IRR = Discounted Cash Flows + Terminal Value - Initial Equity
Equity Multiple = Total Cash Distributions / Initial Equity
```

**Discount Rate (WACC) Reference — UAE Hospitality:**
| Scenario | Discount Rate | Notes |
|---------|--------------|-------|
| Prime Miral-owned asset | 8.5–10.0% | Low risk; government-backed destination |
| Third-party on Miral land | 9.5–11.0% | Adds ground lease / master developer risk |
| New development | 11.0–13.0% | Construction + ramp risk |
| Distressed / repositioning | 12.0–15.0% | Higher execution risk |

---

## 4. Sensitivity Matrix Framework

Run sensitivity across these axes for every model:

**Matrix A: Occupancy vs. ADR Growth**
| | ADR -2% | ADR flat | ADR +3% | ADR +5% |
|---|---------|----------|---------|---------|
| Occ -5pp | | | | |
| Occ flat | | | | |
| Occ +3pp | | | | |
| Occ +5pp | | | | |
*Fill with IRR for each cell*

**Matrix B: Exit Cap Rate vs. CapEx Overrun**
| | CapEx -15% | Base CapEx | CapEx +15% | CapEx +25% |
|---|-----------|-----------|------------|------------|
| Exit cap -50bps | | | | |
| Exit cap flat | | | | |
| Exit cap +50bps | | | | |
| Exit cap +100bps | | | | |
*Fill with equity multiple for each cell*

**Key sensitivity rules:**
- Terminal value must not exceed 65–70% of total asset value — if it does, stress exit cap rate
- Test AED depreciation scenario (theoretical, as peg is maintained, but model for conservatism)
- Test Disneyland delay scenario (opening pushed 3 years vs. base case)

---

## 5. Cap Rate Reference — UAE/GCC Hospitality

| Asset Type | Going-in Cap Rate | Stabilised Cap Rate | Terminal Cap Rate | Source |
|------------|------------------|--------------------|--------------------|--------|
| Trophy 5★ UAE (owned freehold) | 5.5–7.0% | 6.0–7.5% | 6.5–8.0% | JLL MENA 2024 |
| Upper Upscale UAE (4★ full-service) | 6.5–8.0% | 7.0–8.5% | 7.5–9.0% | CBRE MENA |
| Select-service / aparthotel UAE | 7.0–8.5% | 7.5–9.0% | 8.0–9.5% | Knight Frank MENA |
| Theme park-adjacent (Miral premium) | 5.5–6.5% | 6.0–7.0% | 6.5–7.5% | Estimated — [VERIFY] |
| Development / forward funding | 7.5–9.5% on completion value | | | |

**Notes:**
- UAE cap rates are compressing vs. 2022 due to strong NOI growth and investor demand
- Miral assets command a premium (lower cap rate) due to government-backed demand drivers
- Ground lease structures add 50–100bps to required cap rate vs. freehold
- Interest rate environment (UAE follows US Fed via AED peg): model debt at SOFR + 200–300bps
  [VERIFY current SOFR and UAE bank lending rates]

---

## 6. Scenario Definitions

### Base Case
- RevPAR growth: 4–5% Yr 1–5, 3% Yr 6–10
- Occupancy: Stabilises at 80–82% (Yas Island portfolio average)
- ADR growth: In line with UAE CPI + 1%
- Disneyland: Excluded (pre-opening)
- F1 contract: Maintained through model period
- CapEx: Per brand standards on schedule
- Exit: Year 10 at market cap rate

### Upside Case (Disneyland Acceleration)
- RevPAR growth: 8–10% in Disneyland opening years
- Occupancy: Sustains 85–88% post-Disneyland opening
- ADR: +15–20% on Yas Island in opening period
- F1 + Disney + events: Full demand stack operating
- CapEx: On schedule (no PIP overruns)
- Exit: Year 10 at compressed cap rate (investor demand premium)

### Downside Case (Demand Shock)
- Triggers: Regional conflict, oil price collapse, pandemic recurrence, attraction closure
- RevPAR: -15 to -25% in stress year; recovery over 3 years
- Occupancy: Drops to 55–65%
- ADR: -10 to -20%
- F1 cancellation: Model 1-year loss of F1 event revenue
- CapEx: Deferred (increases tail-end cost)
- Exit: Year 10 at expanded cap rate (+100bps vs. base)

---

## 7. Key Ratios & Quality Checks

### Before Finalising Any Miral Hotel Model:

**Arithmetic checks:**
- [ ] RevPAR = Occupancy × ADR (cross-check every period)
- [ ] TRevPAR ≥ RevPAR (other revenue is additive)
- [ ] GOP margin = (GOP / Total Revenue) × 100 — should be 30–45% for full-service
- [ ] NOI uses FF&E below the line (do NOT include FF&E above GOP)
- [ ] Cap rate = Year 1 NOI / Price (not EBITDA — NOI is after FF&E reserve)
- [ ] DCF terminal value ≤ 65–70% of total NPV

**Market reasonableness checks:**
- [ ] RevPAR is within ±20% of Yas Island / Saadiyat Island comp benchmarks
- [ ] ADR is denominated in AED and cross-checked vs. current booking.com / OTA rates
- [ ] F1 weekend modelled as a 4-night block (Thu–Sun) at 3–5x BAR premium
- [ ] UAE VAT (5%) and DTCM municipality fee (4–6%) included in revenue deductions
- [ ] Management fee and brand/franchise fee modelled separately (not combined)
- [ ] PIP costs are in AED per key and tied to specific brand (Hilton ≠ IHG ≠ Rotana)

**Miral-specific checks:**
- [ ] Park-stay bundle contribution modelled or noted if excluded
- [ ] Disneyland scenario clearly labelled Base / Upside / Excluded
- [ ] Ground lease terms (if applicable) modelled as fixed charge, not operating expense
- [ ] Miral ownership vs. third-party asset on Miral land clearly stated in executive summary
- [ ] Seasonality curve applied (Nov F1 spike, Jun–Aug trough for non-Yas properties)
- [ ] Ramadan impact on F&B revenue modelled (dates shift annually)
