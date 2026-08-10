"""
prepare_and_analyse.py

Prepares and analyses NESO's Historic GB Generation Mix dataset
(https://www.neso.energy/data-portal/historic-generation-mix).

Filters the raw half-hourly data down to the most recent 5 years, aggregates
it into daily averages for use in the Excel dashboard, and independently
reproduces the two key findings (renewable/carbon-intensity correlation and
seasonal renewable share) in Python as a cross-check against the Excel work.

Outputs:
    generation_mix_daily_5yr.csv  - daily-averaged data, used in Excel
    seasonality_renewable.png     - bar chart, avg renewable % by month
    renewable_vs_carbon.png       - scatter, renewable % vs carbon intensity
"""

import pandas as pd
import matplotlib.pyplot as plt

# ── LOAD ─────────────────────────────────────────────────────────────────
# Raw data is half-hourly (~48 readings/day) straight from the NESO CSV.
df = pd.read_csv('df_fuel_ckan.csv')
df['DATETIME'] = pd.to_datetime(df['DATETIME'])

# ── FILTER TO LAST 5 YEARS ──────────────────────────────────────────────
cutoff = df['DATETIME'].max() - pd.DateOffset(years=5)
df = df[df['DATETIME'] >= cutoff].copy()
print("Filtered range:", df['DATETIME'].min(), "to", df['DATETIME'].max())
print("Rows:", len(df))

# ── ADD GROUPING COLUMNS ────────────────────────────────────────────────
df['date'] = df['DATETIME'].dt.date
df['year'] = df['DATETIME'].dt.year
df['month'] = df['DATETIME'].dt.month
df['month_name'] = df['DATETIME'].dt.strftime('%b')

# Meteorological seasons (Dec-Feb = Winter, etc.), not calendar quarters.
season_map = {12: 'Winter', 1: 'Winter', 2: 'Winter',
              3: 'Spring', 4: 'Spring', 5: 'Spring',
              6: 'Summer', 7: 'Summer', 8: 'Summer',
              9: 'Autumn', 10: 'Autumn', 11: 'Autumn'}
df['season'] = df['month'].map(season_map)

# ── DAILY AGGREGATION FOR EXCEL ─────────────────────────────────────────
# Excel's dashboard runs off this daily-averaged table, not the raw
# half-hourly data above - that's why correlations calculated on `df`
# directly (below) differ very slightly from the Excel figure.
mw_cols = ['GAS', 'COAL', 'NUCLEAR', 'WIND', 'HYDRO', 'IMPORTS', 'BIOMASS',
           'OTHER', 'SOLAR', 'STORAGE', 'GENERATION', 'LOW_CARBON',
           'ZERO_CARBON', 'RENEWABLE', 'FOSSIL']
perc_cols = [c for c in df.columns if c.endswith('_perc')]

daily = df.groupby(['date', 'year', 'month', 'month_name', 'season']).agg(
    {**{c: 'mean' for c in mw_cols},
     **{c: 'mean' for c in perc_cols},
     'CARBON_INTENSITY': 'mean'}
).reset_index()
daily.to_csv('generation_mix_daily_5yr.csv', index=False)
print("Saved generation_mix_daily_5yr.csv", len(daily), "rows")

# ── ANALYSIS 1: CORRELATION BETWEEN RENEWABLE SHARE AND CARBON INTENSITY ──
# Calculated on the raw half-hourly data (df), not the daily-averaged
# table, so this is expected to differ slightly (-0.86) from the Excel
# dashboard's daily-level figure (-0.87).
corr = df['RENEWABLE_perc'].corr(df['CARBON_INTENSITY'])
print(f"\nCorrelation (renewable % vs carbon intensity): {corr:.3f}")

# ── ANALYSIS 2: MONTHLY AVERAGE RENEWABLE SHARE (SEASONALITY CHECK) ──────
monthly_avg = df.groupby('month_name')['RENEWABLE_perc'].mean()
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
               'Oct', 'Nov', 'Dec']
monthly_avg = monthly_avg.reindex(month_order)

plt.figure(figsize=(9, 5))
monthly_avg.plot(kind='bar', color='seagreen')
plt.title('Average Renewable Share by Month (last 5 years)')
plt.ylabel('Renewable share %')
plt.xlabel('Month')
plt.tight_layout()
plt.savefig('seasonality_renewable.png', dpi=150)
plt.show()

# ── ANALYSIS 3: SCATTER OF RENEWABLE % VS CARBON INTENSITY ──────────────
plt.figure(figsize=(7, 6))
plt.scatter(df['RENEWABLE_perc'], df['CARBON_INTENSITY'], alpha=0.1, s=5)
plt.title(f'Renewable Share vs Carbon Intensity (corr = {corr:.2f})')
plt.xlabel('Renewable share (%)')
plt.ylabel('Carbon intensity (gCO2/kWh)')
plt.tight_layout()
plt.savefig('renewable_vs_carbon.png', dpi=150)
plt.show()

# ── QUICK CHECK: SEASONAL WIND VS SOLAR (console output only) ───────────
# Not saved/plotted - just a quick sense-check of wind/solar seasonality
# printed to the console while developing the analysis above.
seasonal_fuel = df.groupby('month_name')[['WIND_perc', 'SOLAR_perc']].mean()
print(seasonal_fuel.reindex(month_order))
