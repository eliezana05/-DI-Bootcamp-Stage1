# %% [markdown]
# # Exercises XP — Titanic preprocessing
#
# Octopus Week 2 · Day 2
#
# [Assignment](https://octopus.developers.institute/courses/collection/254/course/812/section/1694/chapter/3305)
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
# ## Exercise 1 — Duplicate detection
# Follow a single preprocessing narrative. Keep raw data intact. Identity, target and free-text columns are excluded from the final feature matrix. These are descriptive exercises: a predictive workflow must split first and fit imputation/scaling only on its training fold.

# %%
raw=load('titanic')
print('Before:',len(raw),'duplicates:',raw.duplicated().sum())
df=raw.drop_duplicates().copy()
print('After:',len(df))
assert not df.duplicated().any()

# %% [markdown]
# ## Exercise 2 — Missing values
# Age: median imputation is robust to skew. Embarked: fill with its modal category. Cabin: retain an explicit Unknown category rather than invent a cabin. Removal is demonstrated on a separate complete-case copy; it is not used for the main analysis because it discards many passengers.

# %%
display(df.isna().sum().to_frame('missing_before'))
complete_case=df.dropna()
print('Complete-case alternative:',len(complete_case),'rows; main pipeline retains',len(df))
df['Age']=df['Age'].fillna(df['Age'].median())
df['Embarked']=df['Embarked'].fillna(df['Embarked'].mode().iloc[0])
df['Cabin']=df['Cabin'].fillna('Unknown')
display(df.isna().sum().to_frame('missing_after'))

# %% [markdown]
# ## Exercise 3 — Feature engineering
# FamilySize includes the passenger. Title is extracted from Name. Its one-hot encoding is previewed now and merged with other nominal features only after missing values and outliers have been addressed, reconciling the assignment's ordering reminders.

# %%
df['FamilySize']=df['SibSp']+df['Parch']+1
df['Title']=df['Name'].str.extract(r',\s*([^\.]+)\.',expand=False)
display(df[['Name','Title','FamilySize']].head())
display(pd.get_dummies(df['Title'],prefix='Title',dtype=int).head())

# %% [markdown]
# ## Exercise 4 — Outliers
# Use IQR flags diagnostically. Rare large fares may be real, so retain rows and cap Fare at empirical 2nd/98th percentiles for the scaling demonstration. Age is also capped for the demonstration, while original Age remains available for interpretation. Log1p(Fare) is an alternative. Neither an older passenger nor a costly ticket is automatically an error.

# %%
fig,axes=plt.subplots(1,2,figsize=(10,4))
for ax,col in zip(axes,['Age','Fare']):
    sns.boxplot(x=df[col],ax=ax)
savefig('day2_before_outliers')
for col in ['Age','Fare']:
    q1,q3=df[col].quantile([.25,.75]); iqr=q3-q1
    flag=(df[col]<q1-1.5*iqr)|(df[col]>q3+1.5*iqr)
    low,high=df[col].quantile([.02,.98])
    print(col,'IQR flags:',int(flag.sum()),'caps:',low,high,'alternative rows after removal:',int((~flag).sum()))
    df[col+'_capped']=df[col].clip(low,high)
df['Fare_log']=np.log1p(df['Fare_capped'])
display(df[['Age','Age_capped','Fare','Fare_capped','Fare_log']].describe())
fig,axes=plt.subplots(1,2,figsize=(10,4))
sns.boxplot(x=df['Age_capped'],ax=axes[0]); sns.boxplot(x=df['Fare_capped'],ax=axes[1])
savefig('day2_after_outliers')

# %% [markdown]
# ## Exercise 5 — Standardization and normalization
# Standardize capped Age to demonstrate z scores; Age is not assumed to be exactly normal. Min-max scale capped Fare to [0,1]. Scaling changes units, not distribution shape. The encoding and age groups below are computed before the final matrix is assembled.

# %%
from sklearn.preprocessing import StandardScaler,MinMaxScaler
df['Age_z']=StandardScaler().fit_transform(df[['Age_capped']]).ravel()
df['Fare_01']=MinMaxScaler().fit_transform(df[['Fare_capped']]).ravel()
display(df[['Age_z','Fare_01']].describe())

# %% [markdown]
# ## Exercise 6 — Nominal encoding
# Sex, Embarked and Title have no defensible ordinal rank. Use one-hot encoding; do not label-encode arbitrary categories as ordered numbers. Pclass is an existing ordinal class code.

# %%
encoded=pd.get_dummies(df,columns=['Sex','Embarked','Title'],dtype=int)
display(encoded.filter(regex='^(Sex|Embarked|Title)_').head())

# %% [markdown]
# ## Exercise 7 — Age groups
# Use original, imputed Age for interpretable boundaries: child ≤12, teen (12,18], adult (18,60], senior >60. Include age zero for infants. One-hot encode the groups; keep the original age for audit.

# %%
df['AgeGroup']=pd.cut(df['Age'],bins=[0,12,18,60,120],labels=['child','teen','adult','senior'],include_lowest=True)
display(df['AgeGroup'].value_counts(sort=False))
display(pd.get_dummies(df['AgeGroup'],prefix='AgeGroup',dtype=int).head())
from analysis_utils import prepare_titanic
processed,audit=prepare_titanic(raw)
display(pd.Series(audit))
features=processed.drop(columns=['PassengerId','Survived','Age','Fare','Age_capped','Fare_capped'])
assert not features.isna().any().any()
assert all(pd.api.types.is_numeric_dtype(t) for t in features.dtypes)
assert processed['Fare_01'].between(0,1).all()
assert np.isclose(processed['Age_z'].mean(),0)
assert np.isclose(processed['Age_z'].std(ddof=0),1)
processed.to_csv(ROOT/'day2'/'titanic_preprocessed.csv',index=False)
print('Final feature matrix:',features.shape,'; target kept separately:',raw['Survived'].name)
