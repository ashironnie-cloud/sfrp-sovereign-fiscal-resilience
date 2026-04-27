
"""
Merge master panel with downloaded data and construct SFRI/NCS/DCR.

Usage after running 01_download_worldbank_api.py:
    python code/02_construct_indices.py

Outputs:
    data/final_panel_sfrp.csv
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
panel = pd.read_csv(DATA/'sfrp_country_year_panel_v0_1.csv')
wb_path = DATA/'processed_worldbank_wide.csv'
if wb_path.exists():
    wb = pd.read_csv(wb_path)
    panel = panel.merge(wb,on=['iso3','year'],how='left',suffixes=('','_api'))

def zscore_by_year(df, col, reverse=False):
    x = pd.to_numeric(df[col], errors='coerce')
    mean = x.groupby(df['year']).transform('mean')
    std = x.groupby(df['year']).transform('std')
    z = (x-mean)/std.replace(0,np.nan)
    if reverse: z = -z
    return z

positive = {
    'z_gdp_growth':'gdp_growth',
    'z_gross_capital_formation':'gross_capital_formation_gdp',
    'z_manufacturing':'manufacturing_value_added_gdp',
    'z_exports':'exports_gdp',
    'z_reserves':'reserves_months_imports',
    'z_tax':'tax_revenue_gdp',
    'z_gov_effectiveness':'government_effectiveness',
    'z_control_corruption':'control_corruption',
    'z_rule_law':'rule_of_law',
    'z_reg_quality':'regulatory_quality',
    'z_current_account':'current_account_gdp',
}
negative = {
    'z_inflation_safe':'inflation_cpi',
    'z_public_debt_safe':'central_gov_debt_gdp',
    'z_external_debt_safe':'external_debt_gni',
    'z_debt_service_safe':'debt_service_exports',
    'z_short_debt_reserves_safe':'short_term_debt_reserves',
    'z_imports_safe':'imports_gdp',
    'z_fuel_imports_safe':'fuel_imports_merch_imports',
    'z_food_imports_safe':'food_imports_merch_imports',
}
for z,col in positive.items():
    if col in panel.columns: panel[z] = zscore_by_year(panel,col,False)
for z,col in negative.items():
    if col in panel.columns: panel[z] = zscore_by_year(panel,col,True)

def rowmean(cols):
    have=[c for c in cols if c in panel.columns]
    return panel[have].mean(axis=1,skipna=True) if have else np.nan

panel['P_productive_capacity'] = rowmean(['z_gdp_growth','z_gross_capital_formation','z_manufacturing'])
panel['R_resilience_buffers'] = rowmean(['z_reserves','z_current_account'])
panel['L_fiscal_legitimacy'] = rowmean(['z_tax','z_gov_effectiveness','z_control_corruption','z_rule_law'])
panel['M_fiscal_manoeuvrability'] = rowmean(['z_public_debt_safe','z_external_debt_safe','z_debt_service_safe','z_short_debt_reserves_safe'])
panel['V_safe_vulnerability'] = rowmean(['z_imports_safe','z_fuel_imports_safe','z_food_imports_safe','z_external_debt_safe'])
# Conversion capacity: combine export/tax/reserve changes with governance-weighted investment proxy.
for col in ['exports_gdp','tax_revenue_gdp','reserves_months_imports','gross_capital_formation_gdp']:
    if col in panel.columns:
        panel[f'd5_{col}'] = panel.sort_values(['iso3','year']).groupby('iso3')[col].diff(5)
if 'gross_capital_formation_gdp' in panel.columns and 'government_effectiveness' in panel.columns:
    panel['investment_governance_proxy'] = pd.to_numeric(panel['gross_capital_formation_gdp'],errors='coerce') * pd.to_numeric(panel['government_effectiveness'],errors='coerce')
    panel['z_investment_governance_proxy'] = zscore_by_year(panel,'investment_governance_proxy',False)
for col in ['d5_exports_gdp','d5_tax_revenue_gdp','d5_reserves_months_imports','d5_gross_capital_formation_gdp']:
    if col in panel.columns:
        panel[f'z_{col}'] = zscore_by_year(panel,col,False)
panel['C_conversion_capacity'] = rowmean(['z_d5_exports_gdp','z_d5_tax_revenue_gdp','z_d5_reserves_months_imports','z_d5_gross_capital_formation_gdp','z_investment_governance_proxy'])

panel['SFRI_equal_weight'] = panel[['P_productive_capacity','R_resilience_buffers','L_fiscal_legitimacy','M_fiscal_manoeuvrability','C_conversion_capacity','V_safe_vulnerability']].mean(axis=1,skipna=True)
panel['SFRI_weighted'] = (0.15*panel['P_productive_capacity'] + 0.20*panel['R_resilience_buffers'] + 0.15*panel['L_fiscal_legitimacy'] + 0.20*panel['M_fiscal_manoeuvrability'] + 0.20*panel['C_conversion_capacity'] + 0.10*panel['V_safe_vulnerability'])

# Net conversion score and debt conversion ratio. Use z-score components where possible.
gains = rowmean(['z_d5_exports_gdp','z_d5_tax_revenue_gdp','z_d5_reserves_months_imports','z_d5_gross_capital_formation_gdp'])
risks = rowmean(['z_public_debt_safe','z_external_debt_safe','z_debt_service_safe'])
# risk variables are reverse-coded; convert back to risk by multiplying by -1.
panel['NCS_5yr'] = gains - (-risks)
denom = (-risks).replace(0,np.nan)
panel['DCR_5yr'] = gains / denom

panel.to_csv(DATA/'final_panel_sfrp.csv', index=False)
print('wrote', DATA/'final_panel_sfrp.csv', panel.shape)
