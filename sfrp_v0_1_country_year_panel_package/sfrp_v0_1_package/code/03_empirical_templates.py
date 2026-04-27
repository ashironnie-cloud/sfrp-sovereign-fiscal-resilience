
"""
Empirical model templates for SFRP.
Requires final_panel_sfrp.csv from 02_construct_indices.py.
This file is intentionally a template; adapt outcome definitions after data validation.
"""
from pathlib import Path
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT/'data'/'final_panel_sfrp.csv')
df = df.sort_values(['iso3','year'])
df['sfri_lag1'] = df.groupby('iso3')['SFRI_equal_weight'].shift(1)
df['conversion_lag1'] = df.groupby('iso3')['C_conversion_capacity'].shift(1)
df['debt_lag1'] = df.groupby('iso3')['central_gov_debt_gdp'].shift(1)

# Example crisis proxy if currency/inflation columns are available.
if 'inflation_cpi' in df.columns:
    df['inflation_surge'] = (pd.to_numeric(df['inflation_cpi'],errors='coerce') > 20).astype(float)

# Model C: Debt risk conditional on conversion capacity.
# Replace outcome with validated crisis severity measure.
if {'inflation_surge','debt_lag1','conversion_lag1','gdp_per_capita_current_usd'}.issubset(df.columns):
    model = smf.ols('inflation_surge ~ debt_lag1 * conversion_lag1 + gdp_per_capita_current_usd + C(iso3) + C(year)', data=df).fit(cov_type='cluster', cov_kwds={'groups':df['iso3']})
    print(model.summary())
