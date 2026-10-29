# %% [markdown]
# # Exercises XP — Data understanding and import
#
# Octopus Week 2 · Day 1
#
# [Assignment](https://octopus.developers.institute/courses/collection/254/course/812/section/2143/chapter/4784)
#
# Run cells in order. Source datasets are in `../data`; see the root README for setup and provenance.

# %%
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display
ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / 'analysis_utils.py').exists())
sys.path.insert(0, str(ROOT))
sns.set_theme(style='whitegrid')
def load(kind, filename=None, **kwargs):
    files = list((ROOT / 'data' / kind).rglob(filename or '*.csv'))
    if len(files) != 1:
        raise ValueError(f'Select an unambiguous data file: {files}')
    return pd.read_csv(files[0], **kwargs)
def savefig(name):
    target = ROOT / 'figures'
    target.mkdir(exist_ok=True)
    plt.tight_layout()
    plt.savefig(target / (name + '.png'), dpi=140, bbox_inches='tight')
    plt.show()


# %% [markdown]
# ## Exercise 1 — What is data analysis?
# Data analysis is a systematic process of collecting, validating, organizing and examining observations to answer a question. It combines domain knowledge, descriptive statistics, visualization and, where appropriate, statistical inference. A defensible analysis distinguishes a measured association from a causal explanation and records uncertainty and missing information.
#
# It matters because raw records alone do not show whether a change is meaningful. Analysis makes decisions auditable, detects quality problems and helps allocate limited resources. A large sample still needs suitable definitions and a representative sampling process.
#
# Three applications are: **retail**, where sales and margin analysis informs inventory and promotions; **health research**, where trials compare outcomes while accounting for uncertainty; and **weather forecasting**, where historical atmospheric observations support predictions and verification. ECMWF's operational AIFS deployment in 2025 illustrates the last application; see the sourced daily challenge report for detail.

# %% [markdown]
# ## Exercise 2 — Load and inspect the three provided datasets
# The assignment links GitHub mirrors, so no Kaggle credentials are needed. The mental-health file contains mixed-content rows; initial inspection does not silently treat all 108,553 rows as comparable observations.

# %%
sleep=load('sleep')
mental=load('mental_health',low_memory=False)
credit=load('credit','clean_dataset.csv')
for name,df in [('Sleep',sleep),('Mental health',mental),('Credit approvals',credit)]:
    print(name, 'shape:',df.shape)
    display(df.head())
    display(df.isna().sum().to_frame('missing'))
print('Sleep: annual average sleep hours, demographic groups and day types.')
print('Mental health: country/year health estimates; mixed-content rows require cleaning before comparison.')
print('Credit: applicant attributes and an approval outcome, using the supplied cleaned file.')

# %% [markdown]
# ## Exercise 3 — Classify every column
# Measurement role matters more than storage dtype: a numeric identifier or a coded category is qualitative. Year is a discrete time coordinate. The mental-health rate labels describe quantitative measures even when malformed rows force string storage.

# %%
qualitative={
 'Sleep':{'index','Period','Type of Days','Age Group','Activity','Sex'},
 'Mental health':{'index','Entity','Code'},
 'Credit approvals':{'Gender','Married','BankCustomer','Industry','Ethnicity','PriorDefault','Employed','DriversLicense','Citizen','ZipCode','Approved'}
}
for name,df in [('Sleep',sleep),('Mental health',mental),('Credit approvals',credit)]:
    rows=[]
    for col in df.columns:
        is_qual=col in qualitative[name]
        reason=('Identifier or category: arithmetic on the code is not meaningful.' if is_qual else 'Numeric amount, count, rate or time coordinate: differences have meaning.')
        rows.append({'column':col,'type':'qualitative' if is_qual else 'quantitative','reason':reason})
    print(name)
    display(pd.DataFrame(rows))

# %% [markdown]
# ## Exercise 4 — Iris feature classification

# %%
iris=load('iris')
display(iris.head())
display(pd.DataFrame([{'column':c,'type':'qualitative' if c in ['Id','Species'] else 'quantitative','reason':('Row identifier, not a measurement' if c=='Id' else 'Nominal species label' if c=='Species' else 'Continuous flower dimension measured in centimetres')} for c in iris.columns]))

# %% [markdown]
# ## Exercise 5 — Questions supported by the sleep data
# Use **Year** and **Avg hrs per day sleeping** to study change over time, retaining a single sex/age/day-type stratum. Compare **Type of Days** within the same year and demographic stratum for weekday versus weekend differences. **Sex** and **Age Group** support group comparisons, but the “Both” and “15 years and over” aggregates overlap their component groups. They must not be pooled as independent people. **Standard Error** communicates uncertainty; this file contains survey estimates, not individual sleep records.

# %%
print('Observed labels:')
for c in ['Age Group','Sex','Type of Days']:
    print(c, sorted(sleep[c].dropna().unique()))
display(sleep[['Year','Avg hrs per day sleeping','Standard Error','Type of Days','Age Group','Sex']].head())

# %% [markdown]
# ## Exercise 6 — Structured versus unstructured
# | Source | Classification | Reason |
# |---|---|---|
# | Financial reports in Excel | Structured when organized as a table | Named columns and repeated records; narrative notes remain unstructured |
# | Social photographs | Unstructured | Pixel content does not follow a business table schema; metadata may be structured |
# | News articles | Unstructured text | Free narrative, even if dates and authors are structured metadata |
# | Relational inventory database | Structured | Typed columns, keys and constraints |
# | Recorded research interviews | Unstructured | Audio requires transcription and coding |
#
# ## Exercise 7 — Transform unstructured sources
# | Source | Structured representation and rationale |
# |---|---|
# | Travel blog posts | One row per post: author, date, locations, topics and sentiment; extract metadata and named places, preserving text and source URL for review |
# | Customer calls | Transcribe with timestamps and speaker turns; code issue, resolution and satisfaction into call/turn tables; review transcription errors and consent |
# | Handwritten brainstorm | OCR plus human correction; record note ID, author if known, idea, theme and links; retain the scan to audit uncertain handwriting |
# | Cooking video | Segment steps with start/end times; transcribe speech and annotate ingredient, amount, action and temperature; validate units against the video |
#
# Extraction creates useful structure but does not guarantee accuracy; keep original sources and uncertainty flags.

# %% [markdown]
# ## Exercise 8 — Import the provided Titanic train.csv

# %%
titanic=load('titanic')
display(titanic.head())
assert titanic.shape==(891,12)

# %% [markdown]
# ## Exercise 9 — Export to Excel and JSON

# %%
exports=ROOT/'day1'/'exports'
exports.mkdir(exist_ok=True)
sample=pd.DataFrame({'product':['Notebook','Pen','Folder'],'quantity':[3,10,2],'price':[4.5,1.2,2.0]})
sample.to_excel(exports/'products.xlsx',index=False)
sample.to_json(exports/'products.json',orient='records',indent=2)
pd.testing.assert_frame_equal(sample,pd.read_excel(exports/'products.xlsx'),check_dtype=False)
pd.testing.assert_frame_equal(sample,pd.read_json(exports/'products.json'),check_dtype=False)
display(sample)
print('Both exported files were read back and verified.')

# %% [markdown]
# ## Exercise 10 — Read JSON from the supplied URL
# The supplied URL is a ZIP containing JSON. The download script retrieves that exact archive and extracts it; Pandas reads the cached payload. This avoids mistaking ZIP bytes for a JSON document.

# %%
posts=pd.read_json(next((ROOT/'data'/'posts').rglob('*.json')))
display(posts.head(5))
assert len(posts.head(5))==5
