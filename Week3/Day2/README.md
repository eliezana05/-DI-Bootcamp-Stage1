# Week 3 — Day 2: Global Power Plant Analysis

[Open the analysis in Google Colab](https://colab.research.google.com/drive/15apf1xEkkuXlcykGxYMkaGO7Dq4_X45v)

The notebook uses the WRI Global Power Plant Database v1.3.0 archive supplied by Octopus (chapter 3394). Run all cells to reproduce the cleaning, statistics, hypothesis test, time trends, maps and matrix analysis.

## Findings

- 34,936 unique plant records were analyzed.
- The United States has the most recorded plants: 9,833.
- Solar has the most recorded plants by fuel: 10,665.
- Coal has the highest total installed capacity: approximately 1,965,541 MW.
- Mean installed capacity is 843.58 MW for coal and 373.45 MW for gas. The difference is 470.13 MW (Welch test p ≈ 4.1e-109; 95% confidence interval 430.08–510.18 MW).
- Commissioning years are available for 17,447 records, around half of the database. Decade charts therefore describe the dated subset rather than a complete history of electricity generation.
- The first principal component explains 24.1% of the standardized feature variance in the capacity/location/fuel-indicator matrix.

## Methods and interpretation

Pandas imports and cleans records; NumPy handles numerical conversion, group statistics, Boolean filters, matrix multiplication and eigendecomposition. Matplotlib and Seaborn show capacity distributions, country and fuel counts, commissioning-decade shares and geographic locations.

Missing dates and coordinates remain missing and are excluded only from analyses requiring them. Missing generation is not replaced by installed capacity. MW measures power capacity, while GWh measures generated energy; this analysis does not equate them.

The coal/gas comparison is observational. Skew, outliers, country mix and database coverage limit inference; statistical significance does not imply fuel causes capacity differences. Commissioning charts reflect the plants represented in the snapshot, including reporting and survival biases. PCA depends on scaling and fuel coding and does not identify causal drivers.

## Validation

All cells ran successfully in Colab. Checks cover unique plant identifiers, finite nonnegative capacity, matrix correlation diagonals and the eigenvector equation.
