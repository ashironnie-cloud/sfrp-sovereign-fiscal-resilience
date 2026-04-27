
"""
Download World Bank API indicators for the Sovereign Fiscal Resilience Panel.

Usage:
    python code/01_download_worldbank_api.py

Notes:
    - Requires internet access and requests/pandas.
    - The current ChatGPT sandbox cannot resolve external API hosts; this script is designed to run locally or on a connected server.
    - Outputs data/processed_worldbank_long.csv and data/processed_worldbank_wide.csv.
"""
import json, time
from pathlib import Path
import requests
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
indicator_map = json.loads((ROOT/'docs'/'world_bank_indicator_map.json').read_text())
countries = pd.read_csv(DATA/'country_master.csv')['iso3'].tolist()
country_str = ';'.join(countries)
rows=[]

def fetch_indicator(indicator):
    page=1
    while True:
        url=(f'https://api.worldbank.org/v2/country/{country_str}/indicator/{indicator}'
             f'?format=json&per_page=20000&page={page}')
        r=requests.get(url,timeout=60)
        r.raise_for_status()
        payload=r.json()
        if not isinstance(payload,list) or len(payload)<2:
            return
        meta, data = payload[0], payload[1]
        for obs in data:
            rows.append({
                'iso3': obs.get('countryiso3code'),
                'country_name_api': (obs.get('country') or {}).get('value'),
                'year': int(obs.get('date')) if obs.get('date') else None,
                'indicator_code': indicator,
                'variable_name': indicator_map[indicator],
                'value': obs.get('value')
            })
        if page >= int(meta.get('pages',1)):
            break
        page += 1
        time.sleep(0.2)

for ind in indicator_map:
    print('fetching', ind, indicator_map[ind])
    fetch_indicator(ind)

long = pd.DataFrame(rows)
DATA.mkdir(exist_ok=True)
long.to_csv(DATA/'processed_worldbank_long.csv',index=False)
wide = long.pivot_table(index=['iso3','year'],columns='variable_name',values='value',aggfunc='first').reset_index()
wide.to_csv(DATA/'processed_worldbank_wide.csv',index=False)
print('wrote', DATA/'processed_worldbank_wide.csv', wide.shape)
