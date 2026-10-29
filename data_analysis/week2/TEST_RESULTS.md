# Verification — 29 October 2026

- Seven notebooks executed from first to last cell with fresh Jupyter kernels; no failed or unexecuted code cells.
- Four unit tests passed for Titanic duplicate/missing-value handling, encoding and scaling; salary normalization including constant input; invalid crash survival denominators; and Superstore zero-sales margins/date parsing.
- Coverage of `analysis_utils.py`: 46 statements, 0 missed, **100% statement coverage**. This figure applies to the shared preprocessing functions, not all notebook prose or plotting code.
- Eighteen saved chart figures reviewed visually; the notebooks also preserve interactive-widget default output and embedded images.
- Day 1 Excel and JSON exports read back and compared to the source DataFrame.
- Dataset hashes and schema/dimension checks recorded; Titanic shape checked as 891 × 12.
- Normalization bounds, standardization moments, final feature missingness/numeric types and binomial probability checked with assertions.
- Source-column mismatches handled: the student file uses `Do you have Panic attack?`; US Superstore dates parsed explicitly; crash file read with Windows-compatible encoding.
- Salary currencies inspected and separated for monetary comparisons; no invented exchange rates.

Reproduce the unit verification from this folder:

```sh
python -m coverage run --source=analysis_utils -m unittest -v test_analysis.py
python -m coverage report
python run_all.py
```

Environment versions are pinned in `requirements.txt`. This verifies execution and specified invariants; it does not independently reproduce the external ECMWF experiment or establish causal claims from observational datasets.
