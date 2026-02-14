import unittest
from regdbot.brain import analysis
import pandas as pd

class TestEDA(unittest.TestCase):
    def test_instantiate_EDA(self):
        df = pd.read_csv('brain/fixtures/Star_Trek_Season_1.csv')
        eda = analysis.EDA(df)
        self.assertIsInstance(eda.df_filtered, pd.DataFrame)
        self.assertIsInstance(eda.mostly_null_cols, list)
        self.assertIsInstance(eda.numerical_columns, pd.Index)
        self.assertIsInstance(eda.categorical_columns, pd.Index)
