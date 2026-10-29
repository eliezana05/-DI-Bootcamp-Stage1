"""Small, tested preprocessing functions used by the submitted notebooks."""
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler


def normalize_salary(series):
    """Min-max normalize a numeric salary series; a constant series becomes zero."""
    return MinMaxScaler().fit_transform(series.to_numpy().reshape(-1, 1)).ravel()


def prepare_titanic(frame):
    """Descriptive preprocessing; fit on training folds only for predictive use."""
    df = frame.drop_duplicates().copy()
    audit = {'rows_before': len(frame), 'duplicates_removed': len(frame)-len(df)}
    df['Age'] = df['Age'].fillna(df['Age'].median())
    df['Fare'] = df['Fare'].fillna(df['Fare'].median())
    df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode().iloc[0])
    df['Cabin'] = df['Cabin'].fillna('Unknown')
    df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
    df['Title'] = df['Name'].str.extract(r',\s*([^\.]+)\.', expand=False).fillna('Unknown')
    df['AgeGroup'] = pd.cut(df['Age'], bins=[0,12,18,60,120], labels=['child','teen','adult','senior'], include_lowest=True)
    for col in ['Age','Fare']:
        low, high = df[col].quantile([.02,.98])
        audit[col+'_caps'] = [float(low),float(high)]
        df[col+'_capped'] = df[col].clip(low,high)
    df['Fare_log'] = np.log1p(df['Fare_capped'])
    df['Age_z'] = StandardScaler().fit_transform(df[['Age_capped']]).ravel()
    df['Fare_01'] = MinMaxScaler().fit_transform(df[['Fare_capped']]).ravel()
    df = pd.get_dummies(df.drop(columns=['Name','Cabin','Ticket'],errors='ignore'), columns=['Sex','Embarked','Title','AgeGroup'],dtype=int)
    audit['rows_after'] = len(df)
    return df,audit


def clean_crashes(frame):
    """Keep unknown fatality counts unknown and reject invalid survival denominators."""
    df=frame.drop_duplicates().copy()
    df['Date']=pd.to_datetime(df['Date'],format='%m/%d/%Y',errors='coerce')
    for col in ['Aboard','Fatalities','Ground']:
        if col in df:
            df[col]=pd.to_numeric(df[col],errors='coerce')
            df.loc[df[col]<0,col]=np.nan
    df['Year']=df['Date'].dt.year
    df['Decade']=(df['Year']//10)*10
    valid=(df['Aboard']>0)&df['Fatalities'].between(0,df['Aboard'])
    df['SurvivalRate']=((df['Aboard']-df['Fatalities'])/df['Aboard']).where(valid)
    return df


def prepare_superstore(frame):
    df=frame.drop_duplicates().copy()
    for col in ['Order Date','Ship Date']:
        df[col]=pd.to_datetime(df[col],format='%m/%d/%Y',errors='coerce')
    df['Profit Margin']=df['Profit'].div(df['Sales'].replace(0,np.nan))*100
    df['Order Year']=df['Order Date'].dt.year
    df['Order Month']=df['Order Date'].dt.month
    df['Order Month-Year']=df['Order Date'].dt.to_period('M')
    return df
