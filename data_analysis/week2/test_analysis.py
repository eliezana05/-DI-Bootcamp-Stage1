import unittest
import numpy as np
import pandas as pd
from analysis_utils import prepare_titanic, normalize_salary, clean_crashes, prepare_superstore


class AnalysisTests(unittest.TestCase):
    def test_titanic_deduplicates_imputes_and_encodes(self):
        frame = pd.DataFrame({'Age':[10,np.nan,90], 'Fare':[0,10,999], 'SibSp':[0,1,0], 'Parch':[0,1,0], 'Name':['A, Mr. X','B, Mrs. Y','C, Dr. Z'], 'Sex':['male','female','male'], 'Embarked':['S',np.nan,'C'], 'Cabin':[np.nan,'A1',np.nan]})
        result, audit = prepare_titanic(pd.concat([frame,frame.iloc[[0]]],ignore_index=True))
        self.assertEqual(len(result),3)
        self.assertEqual(audit['duplicates_removed'],1)
        self.assertEqual(result['FamilySize'].tolist(),[1,3,1])
        self.assertFalse(result.isna().any().any())
        self.assertTrue(result['Age_z'].mean().round(10)==0)
        self.assertTrue(result['Fare_01'].between(0,1).all())
        self.assertEqual(result.filter(like='AgeGroup_').sum(axis=1).tolist(),[1,1,1])

    def test_salary_normalization_constant_and_bounds(self):
        np.testing.assert_allclose(normalize_salary(pd.Series([10,20,30])),[0,.5,1])
        np.testing.assert_allclose(normalize_salary(pd.Series([5,5])),[0,0])

    def test_crashes_invalid_denominator_and_counts(self):
        df=pd.DataFrame({'Date':['1/1/2000','bad','2/1/2010','3/1/2010'], 'Aboard':[10,0,2,10], 'Fatalities':[4,0,4,np.nan]})
        out=clean_crashes(df)
        self.assertAlmostEqual(out.loc[0,'SurvivalRate'],.6)
        self.assertTrue(out.loc[1:,'SurvivalRate'].isna().all())
        self.assertTrue(pd.isna(out.loc[1,'Date']))
        self.assertTrue(pd.isna(out.loc[3,'Fatalities']))

    def test_superstore_zero_sales_and_dates(self):
        df=pd.DataFrame({'Order Date':['01/02/2020','02/03/2020'], 'Ship Date':['01/03/2020','02/04/2020'], 'Sales':[100,0], 'Profit':[10,-1]})
        out=prepare_superstore(df)
        self.assertEqual(out.loc[0,'Profit Margin'],10)
        self.assertTrue(pd.isna(out.loc[1,'Profit Margin']))
        self.assertEqual(out.loc[0,'Order Month'],1)

if __name__=='__main__': unittest.main()
