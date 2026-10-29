# Week 2 — Data Analysis: Days 1–4

Eight Octopus assignments marked **SUBMIT**, completed on 29 October 2026. The original Python exercises elsewhere in the repository are independent.

| Day | Exercises XP | Daily challenge |
|---|---|---|
| 1 | [10 exercises: data understanding, types, CSV/JSON imports and Excel/JSON exports](day1/exercises_xp.ipynb) | [Real-world Data Analysis Scenarios — sourced ECMWF case](day1/daily_challenge.md) |
| 2 | [7 Titanic preprocessing exercises](day2/exercises_xp.ipynb) | [Data Handling and Analysis in Python — salaries, PCA, aggregation](day2/daily_challenge.ipynb) |
| 3 | [8 SciPy exercises, including optional questions 7–8](day3/exercises_xp.ipynb) | [Analysis of Airplane Crashes](day3/daily_challenge.ipynb) |
| 4 | [6 Matplotlib/Seaborn exercises](day4/exercises_xp.ipynb) | [Strategic Analysis of Superstore Performance](day4/daily_challenge.ipynb) |

The seven notebooks include executed outputs and embedded charts, readable on GitHub without rerunning. Matching `.py` exports contain the same code and explanatory comments. The Day 1 written challenge is a Markdown report. The Superstore notebook includes a category dropdown and Top N slider for a live Jupyter session, with static chart outputs for GitHub.

## Scope exclusions

The XP Gold and XP Ninja pages for all four days display **Click here to Complete**, not SUBMIT. Day 1's additional **Hands-On Image Transformation and Visualization** challenge has the same non-submission status. These were inspected and excluded, as requested. Day 5, course notes, online learning and remote learning are outside this scope. The optional questions within Day 3's submitted XP page are included; the optional advanced Superstore additions are not required.

## Reproduce in VS Code / Jupyter

From this folder (Python 3.11 or later; verified with Python 3.15):

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python download_data.py
python -m ipykernel install --prefix "$VIRTUAL_ENV" --name python3
python run_all.py
python -m unittest -v test_analysis.py
```

Open this folder in VS Code and select the `.venv` Python kernel for a notebook. The executed results are already saved; rerunning the downloaded project requires downloading datasets first. Live widget interaction requires a Jupyter frontend supporting ipywidgets; GitHub shows saved static figures only.

The download script uses the exact Octopus source mirrors, resolving their Git LFS files through GitHub's media endpoint. Superstore is downloaded from the assignment's public Kaggle dataset. `SOURCES.json` records archive and extracted-file SHA-256 hashes and URLs. Original data is excluded from Git to avoid redistributing third-party datasets; download links and hashes support reproduction. Generated figures are embedded in notebooks. The Excel and JSON exports are included.

## Analytical choices

- Classify columns by meaning, not merely their numeric/string storage type. IDs and coded categories are qualitative.
- Titanic: missingness audit, median/mode/Unknown demonstrations, outlier diagnostics, justified capping, feature engineering, nominal encoding and scale checks. Predictive use requires fitting transformations inside a training split.
- Salaries: the source contains USD, EUR and GBP. Group statistics retain currency; the comparative chart and PCA use USD only. Two-component PCA loses substantial information, which is reported.
- Crashes: unknown fatalities stay missing; invalid survival denominators are excluded, with counts reported. Event severity is not flight risk. Welch and Mann–Whitney test different hypotheses.
- Student data: CGPA intervals remain categories; anxiety charts show within-group proportions. The actual panic-attack column spelling is used.
- Superstore: explicit US dates, weighted overall profit margin, order-line granularity, category-aware discount diagnostics and qualified business recommendations. See [executive summary](day4/executive_summary.md).

## Verification and submission

See [TEST_RESULTS.md](TEST_RESULTS.md) for executed checks. Assignment URLs appear inside every deliverable. All eight assignment folders/files can be submitted by linking the relevant path in GitHub to Octopus. No Octopus submission or completion button has been activated automatically.
