# %% [markdown]
# # Daily challenge — Strategic Superstore analysis
#
# Octopus Week 2 · Day 4
#
# [Assignment](https://octopus.developers.institute/courses/collection/254/course/812/section/1705/chapter/4339)
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
# ## Business questions and scope
# Which categories and states contribute sales, which products contribute profit, and which observed discount bands coincide with losses? Analyze order lines, not unique orders or customers. Dataset currency is USD. Recommendations are diagnostic hypotheses; discount allocation is not randomized, so correlation does not establish the effect of changing prices.

# %%
raw=load('superstore',encoding='cp1252')
print('Shape:',raw.shape);print('Columns:',raw.columns.tolist());raw.info()
display(raw.head(3));display(raw.describe());display(raw.isna().sum().to_frame('missing'))
print('Duplicate full rows:',raw.duplicated().sum())

# %% [markdown]
# ## Preparation and feature engineering
# Remove exact duplicate records only. Preserve repeated orders because one order may contain multiple lines. Parse US-format dates explicitly. Keep missing postal codes unknown rather than inventing location 0; they are not used for these aggregations. Sales=0 produces an undefined margin (NaN), not infinity. The overall business margin is total profit / total sales, not an unweighted average of line margins.

# %%
from analysis_utils import prepare_superstore
df=prepare_superstore(raw)
assert df['Order Date'].notna().all()
print('Date range:',df['Order Date'].min(),df['Order Date'].max())
display(df[['Sales','Profit','Profit Margin','Order Year','Order Month']].head())
print('Rows after cleaning:',len(df),'unique orders:',df['Order ID'].nunique())

# %% [markdown]
# ## Monthly sales: category dropdown
# The initial chart is saved as a static figure for GitHub. In Jupyter, the dropdown recalculates the series. Missing calendar months are filled with zero in the displayed period.

# %%
import ipywidgets as widgets
def plot_monthly_sales(category='All'):
    selected=df if category=='All' else df[df['Category']==category]
    monthly=selected.groupby('Order Month-Year')['Sales'].sum()
    index=pd.period_range(df['Order Month-Year'].min(),df['Order Month-Year'].max(),freq='M')
    monthly=monthly.reindex(index,fill_value=0)
    fig,ax=plt.subplots(figsize=(11,4))
    ax.plot(monthly.index.to_timestamp(),monthly.to_numpy(),marker='o',markersize=3)
    ax.set(title=f'Monthly sales — {category}',xlabel='Month',ylabel='Sales (USD)')
    fig.autofmt_xdate()
    plt.tight_layout();plt.show()
    return monthly
monthly=plot_monthly_sales()
widgets.interact(plot_monthly_sales,category=widgets.Dropdown(options=['All']+sorted(df['Category'].unique()),value='All',description='Category'))
fig,ax=plt.subplots(figsize=(11,4));ax.plot(monthly.index.to_timestamp(),monthly.values)
ax.set(title='Monthly Superstore sales — all categories',xlabel='Month',ylabel='Sales (USD)');fig.autofmt_xdate()
savefig('day4_superstore_monthly')
display(df.groupby('Order Year')[['Sales','Profit']].sum().round(2))
display(df.groupby('Order Month')['Sales'].sum().sort_values(ascending=False).to_frame('sales_by_calendar_month'))

# %% [markdown]
# ## Geographic concentration: Top N slider

# %%
state_sales=df.groupby('State')['Sales'].sum().sort_values()
def plot_top_states(top_n=10):
    values=state_sales.tail(top_n)
    fig,ax=plt.subplots(figsize=(10,max(4,top_n*.28)))
    bars=ax.barh(values.index,values.values,color='steelblue')
    ax.bar_label(bars,labels=[f'${v:,.0f}' for v in values],padding=3)
    ax.set(xlabel='Sales (USD)',ylabel='State',title=f'Top {top_n} states by sales')
    ax.margins(x=.18);plt.tight_layout();plt.show()
widgets.interact(plot_top_states,top_n=widgets.IntSlider(min=5,max=min(25,len(state_sales)),value=10,description='Top N'))
print('Top five share:',state_sales.tail(5).sum()/state_sales.sum())
state_sales.tail(10).plot.barh(figsize=(9,5));plt.xlabel('Sales (USD)');plt.title('Ten largest state markets')
savefig('day4_superstore_states')

# %% [markdown]
# ## Ten most profitable products
# Group by Product ID and Product Name to avoid merging different IDs with the same name. Exact profit values are annotated.

# %%
product_profit=df.groupby(['Product ID','Product Name'])['Profit'].sum().nlargest(10)
labels=[name for _,name in product_profit.index]
fig,ax=plt.subplots(figsize=(12,7))
sns.barplot(x=product_profit.values,y=labels,hue=labels,palette='viridis',legend=False,ax=ax)
for container in ax.containers:
    ax.bar_label(container,fmt='$%.2f',padding=4)
ax.set(title='Top ten products by total profit',xlabel='Profit (USD)',ylabel='Product')
ax.margins(x=.2)
savefig('day4_superstore_products')
display(product_profit.to_frame('profit'))

# %% [markdown]
# ## Discounts and losses
# Show category colors and category-specific fitted lines, plus the overall regression. Tabulate each observed discount level by category with sample size, average profit and loss share. A threshold is a candidate for investigation, not a guaranteed safe discount or a causal estimate.

# %%
fig,ax=plt.subplots(figsize=(11,6))
sns.scatterplot(data=df,x='Discount',y='Profit',hue='Category',alpha=.35,s=20,ax=ax)
sns.regplot(data=df,x='Discount',y='Profit',scatter=False,ci=None,color='black',ax=ax,line_kws={'linestyle':'--','label':'Overall fit'})
for category,color in zip(sorted(df['Category'].unique()),sns.color_palette(n_colors=3)):
    sns.regplot(data=df[df['Category']==category],x='Discount',y='Profit',scatter=False,ci=None,color=color,ax=ax)
ax.axhline(0,color='grey');ax.set(title='Discount and line profit by category',xlabel='Discount fraction',ylabel='Profit (USD)')
savefig('day4_superstore_discounts')
discounts=df.assign(Loss=df['Profit']<0).groupby(['Category','Discount']).agg(n=('Profit','size'),mean_profit=('Profit','mean'),loss_share=('Loss','mean'))
display(discounts.round(3))
discounts.to_csv(ROOT/'day4'/'discount_diagnostics.csv')
high=df[df['Discount']>.2]
display(high.groupby('Category')['Profit'].agg(['count','mean','sum']))
print('High discount (>20%) loss share:',(high['Profit']<0).mean())

# %% [markdown]
# ## Tooling review — Matplotlib and Seaborn
# Matplotlib offers direct control of axes, annotations and layouts; it works well with explicit widget callbacks. Seaborn expresses grouped and statistical plots succinctly and handles semantic colors and legends. Both integrate with ipywidgets through Python callbacks; interactivity is not exclusive to either. Rendering speed depends on the chart, backend and data, so one timing is not a general performance claim. Here Matplotlib fits the custom time/state charts and Seaborn fits the grouped discount comparison. For executive communication, titles, units, denominators and restrained color choices matter more than library choice.

# %% [markdown]
# ## Executive summary — computed findings and actions

# %%
total_sales=df['Sales'].sum();total_profit=df['Profit'].sum()
annual=df.groupby('Order Year')['Sales'].sum()
best_month=int(df.groupby('Order Month')['Sales'].sum().idxmax())
top_category=df.groupby('Category')['Sales'].sum().idxmax()
summary=f"""# Executive summary

- Revenue is ${total_sales:,.2f}; profit is ${total_profit:,.2f}; aggregate profit margin is {total_profit/total_sales:.2%}.
- {state_sales.index[-1]} is the largest state market (${state_sales.iloc[-1]:,.2f}); the top five states account for {state_sales.tail(5).sum()/total_sales:.1%} of revenue. Protect availability in these markets while evaluating profit, not revenue alone.
- {top_category} leads category sales. The most profitable product is {product_profit.index[0][1]}, contributing ${product_profit.iloc[0]:,.2f}. Review stock availability and concentration risk.
- Sales change from ${annual.iloc[0]:,.0f} in {annual.index[0]} to ${annual.iloc[-1]:,.0f} in {annual.index[-1]}; calendar month {best_month} has the largest pooled sales. Plan inventory around recurring peaks, but distinguish year growth from seasonal effects.
- {(high['Profit']<0).mean():.1%} of order lines discounted above 20% lose money. Review category-specific high-discount promotions and run a controlled pilot before imposing a universal cap; observed association is not causal.

Limitations: this historical sample is not current store performance. Returns, acquisition cost, inventory constraints and exposure are not fully modeled. Validate margin definitions and test the promotion hypothesis with appropriate controls.
"""
from IPython.display import Markdown
display(Markdown(summary))
(ROOT/'day4'/'executive_summary.md').write_text(summary)
print('All notebook analyses completed.')
