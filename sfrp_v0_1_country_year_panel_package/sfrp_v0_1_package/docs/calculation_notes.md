
# Calculation Notes

## Sovereign Fiscal Resilience Index

The equal-weight index is:

SFRI_it = mean(P_it, R_it, L_it, M_it, C_it, Vsafe_it)

where:
- P = productive capacity
- R = resilience buffers
- L = fiscal legitimacy / state capacity
- M = fiscal manoeuvrability
- C = conversion capacity
- Vsafe = reverse-coded structural vulnerability

## Net Conversion Score

NCS_5yr = (Delta P + Delta R + Delta X + Delta T) - (Delta D + Delta F)

In the empirical implementation, these are measured using normalised changes in productive, export, reserve and tax indicators, minus normalised increases in debt/risk indicators.

## Debt Conversion Ratio

DCR_5yr = (Delta P + Delta R + Delta X + Delta T) / (Delta D + Delta F)

Because ratios can become unstable if the denominator is small, NCS_5yr should be the main empirical measure and DCR_5yr should be treated as a diagnostic.

## Qualitative scorecard mean

scorecard_mean_8 = average(legitimacy, weather/buffers, terrain/productive capacity, command/state capacity, doctrine/fiscal framework, track record, conversion capacity, resilience)

These scores are provisional and should not be treated as final econometric estimates.
