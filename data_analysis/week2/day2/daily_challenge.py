# %% [markdown]
# # Daily challenge — Data science salaries
#
# Octopus Week 2 · Day 2
#
# [Assignment](https://octopus.developers.institute/courses/collection/254/course/812/section/1694/chapter/3308)
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
# ## Import, explore and clean
# Use the exact salary dataset provided by Octopus. Remove a CSV index column, but retain repeated job listings because no unique listing identifier establishes that they are errors. Check currencies before aggregating monetary values. Never compare mixed local currencies as if they were the same unit.

# %%
salary=load('salaries').drop(columns=['Unnamed: 0'],errors='ignore')
display(salary.head()); display(salary.describe(include='all'))
print('Missing:',salary.isna().sum().to_dict())
print('Repeated attribute rows:',salary.duplicated().sum())
print('Currencies:',salary['salary_currency'].value_counts().to_dict())
assert salary['salary'].notna().all() and (salary['salary']>=0).all()

# %% [markdown]
# ## Min-max salary normalization

# %%
from analysis_utils import normalize_salary
salary['salary_normalized']=normalize_salary(salary['salary'])
display(salary[['salary','salary_normalized']].head())
assert np.isclose(salary['salary_normalized'].min(),0) and np.isclose(salary['salary_normalized'].max(),1)

# %% [markdown]
# ## Dimensionality reduction with PCA
# Drop the redundant normalized salary from PCA input, encode job/experience/location/currency/type categorically, then standardize the encoded feature matrix before projecting onto two components. PCA uses USD listings only so the numeric salary feature has a consistent unit. This is exploratory PCA; a model predicting salary must exclude salary itself and fit preprocessing on training data only. Coordinates of one-hot PCA are not causal factors.

# %%
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
pca_salary=salary[salary['salary_currency']=='USD'].copy()
x=pd.get_dummies(pca_salary.drop(columns=['salary_normalized','salary_currency']),dtype=float)
scaled=StandardScaler().fit_transform(x)
pca=PCA(n_components=2,svd_solver='full')
coords=pca.fit_transform(scaled)
print('Original dimensions:',x.shape[1],'; reduced dimensions:',coords.shape[1])
print('Explained variance:',pca.explained_variance_ratio_, '; total:',pca.explained_variance_ratio_.sum())
display(pd.DataFrame(coords,columns=['PC1','PC2']).head())
sns.scatterplot(x=coords[:,0],y=coords[:,1],hue=pca_salary['experience_level'],alpha=.5)
plt.title('Salary dataset: two-component PCA');plt.xlabel('PC1');plt.ylabel('PC2')
savefig('day2_salary_pca')

# %% [markdown]
# ## Experience-level aggregation
# Report mean, median and count by experience and currency, preserving monetary units. Counts help distinguish well-represented roles from sparse categories. The unadjusted differences may reflect location and job-title composition.

# %%
summary=salary.groupby(['salary_currency','experience_level'])['salary'].agg(['count','mean','median']).round(2)
display(summary)
summary.to_csv(ROOT/'day2'/'salary_summary.csv')
g=salary[salary['salary_currency']=='USD'].groupby('experience_level')['salary'].median().sort_values()
g.plot.barh();plt.xlabel('Median listed salary (USD listings only)');plt.title('Median USD salary by experience')
savefig('day2_salary_by_experience')
print('Highest median USD group:',g.index[-1],f'({g.iloc[-1]:,.0f})')
print('Lowest median USD group:',g.index[0],f'({g.iloc[0]:,.0f})')
print('PCA keeps',f'{pca.explained_variance_ratio_.sum():.1%}','of standardized variance: two axes lose information.')

# %% [markdown]
# ## Interpretation
# Normalization places observed salaries on a common numeric range but does not remove location, role or seniority effects. PCA demonstrates compression rather than a salary prediction. Use the displayed currency-aware table to compare experience groups; this convenience sample of listings is not an estimate of all workers' pay. Validate missing compensation, selection bias and repeated listings before recruitment policy decisions.
