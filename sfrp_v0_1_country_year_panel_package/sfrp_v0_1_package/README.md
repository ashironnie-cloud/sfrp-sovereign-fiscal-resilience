
# Sovereign Fiscal Resilience Panel (SFRP) v0.1

This package is the first reproducible dataset build for the paper **Sovereign Fiscal Resilience and Debt Conversion: Theory and Evidence**.

## What is included now

- `data/country_master.csv` - country list, classifications and case flags.
- `data/qualitative_scorecards.csv` - provisional 1-5 country scorecards for the core paper countries.
- `data/sfrp_country_year_panel_v0_1.csv` - country-year master panel, 1980-2025, with metadata and provisional scorecard variables.
- `docs/data_dictionary.csv` - variable definitions and transformations.
- `docs/source_log.csv` - source inventory and URLs.
- `docs/world_bank_indicator_map.json` - World Bank/WGI/IDS indicator-code map.
- `code/01_download_worldbank_api.py` - downloader for WDI/WGI/IDS indicators using the World Bank API.
- `code/02_construct_indices.py` - SFRI, DCR and NCS construction script.
- `code/03_empirical_templates.py` - first regression-template file.

## Important status note

The ChatGPT execution sandbox used to create this package could not resolve external API hosts. Therefore, this v0.1 package contains the complete master panel, qualitative scorecard layer, data dictionary, source map and runnable ingestion scripts, but the macroeconomic source variables will populate only after `01_download_worldbank_api.py` is run in a connected Python environment.

## Recommended run order

```bash
cd sfrp_v0_1_package
python code/01_download_worldbank_api.py
python code/02_construct_indices.py
python code/03_empirical_templates.py
```

## Main empirical objects

- `SFRI_equal_weight`: equal-weight Sovereign Fiscal Resilience Index.
- `SFRI_weighted`: weighted Sovereign Fiscal Resilience Index.
- `C_conversion_capacity`: conversion-capacity sub-index.
- `NCS_5yr`: five-year Net Conversion Score.
- `DCR_5yr`: five-year Debt Conversion Ratio.

## Interpretation guardrails

- The qualitative scorecards are pilot classification instruments, not causal evidence.
- The econometric paper should use the quantitative SFRI/DCR/NCS variables after source ingestion.
- External debt and debt-service variables should be treated as especially important for small open economies and developing countries.
- All crisis indicators require careful validation against source definitions before publication.
