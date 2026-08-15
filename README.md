# GB Electricity Generation Mix — 5-Year Analysis (2021-2026)

## Overview
An Excel-based analysis and dashboard exploring 5 years of daily electricity generation data for Great Britain, analysing the relationship between renewable generation, carbon intensity, and seasonal demand patterns. ![Dashboard](dashboard.png)

## Data Source
[National Energy System Operator (NESO) — Historic GB Generation Mix](https://www.neso.energy/data-portal/historic-generation-mix), released under the NESO Open Data Licence. The full NESO dataset runs from 2009 onward; this project uses a 5-year subset (2021-2026).

## Methodology
- Structured ~1,827 days of generation-mix data (by fuel type: gas, coal, nuclear, wind, hydro, solar, biomass, etc.) in Excel
- Built pivot tables to summarise generation mix, renewable share, and carbon intensity by season and by month
- Calculated correlation between `RENEWABLE_perc` and `CARBON_INTENSITY` using Excel's `CORREL` function
- Built a scatter chart, seasonal demand/gas combo chart, and monthly nuclear-output chart to visualise patterns
- Assembled findings into a single-page dashboard with KPI summary cards

## Key Findings

**1. Renewables and carbon intensity are strongly inversely linked (r = -0.87)**
Across all 1,827 days, higher renewable generation share consistently tracked with lower carbon intensity. This is expected directionally — renewables displace fossil generation — but the strength of the correlation (close to -1) confirms just how tightly the two move together, with day-to-day variation explained by wind/solar output more than any other single factor.

**2. Carbon intensity fell for four straight years, then reversed in 2025**
Average carbon intensity dropped every year from 2021 to 2024 (178 → 124 gCO2/kWh), driven by rising renewable share. That trend broke in 2025: nuclear output fell to its lowest level in decades, and gas generation increased to cover the gap, pushing average carbon intensity back up. It's a reminder that a falling-carbon-intensity trend depends on the whole generation mix, not renewables alone — a nuclear shortfall can undo years of renewable-driven progress.

**3. Autumn has the highest gas dependency (31.7%), despite Winter having the highest demand**
Total demand peaks in Winter at 36,421 MW, as expected, but gas's share of the generation mix peaks in Autumn at 31.7%, even though Autumn's demand is only 32,411 MW. Winter's wind share (27.6%) is higher than Autumn's (24.4%), a gap of 3.2 percentage points — so Winter's extra demand is largely covered by strong wind output, while Autumn, a transitional season with comparatively weaker wind, must lean harder on gas to fill the gap. This complicates the common "cold weather drives gas use" assumption and shows the value of testing it against the data directly.

## Python Cross-Check
The same analysis was independently reproduced in Python to validate the Excel findings. Correlation was calculated at two different levels of granularity — Excel's dashboard uses the daily-averaged dataset (-0.87), while the Python figure (-0.86) was calculated on the raw half-hourly data before aggregation. The near-identical result across both confirms the relationship holds regardless of aggregation level.

![Renewable vs Carbon Intensity](renewable_vs_carbon.png)
![Monthly Renewable Share](seasonality_renewable.png)

## Tools
Excel (pivot tables, formulas, charts, dashboard layout). Python (data analysis — script included).

## Author
Katie Lovell — Maths & Physics student, University of Liverpool.
