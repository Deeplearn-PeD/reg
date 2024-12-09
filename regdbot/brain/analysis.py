"""
This module contains functions for analyzing data from the database.
"""
from typing import List, Tuple, Any,  Dict, Optional
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from scipy import stats
from sqlalchemy import create_engine

try:
    globals()['__IPYTHON__']
    _not_in_ipython = False
except KeyError:
    _not_in_ipython = True
    matplotlib.use("svg")


def get_data_from_db(table_name: str, connection_string: str) -> pd.DataFrame:
    """
    Connect to the database and fetch data from a specific table.
    :param table_name: Name of the table to fetch data from.
    :param connection_string: The connection string to the database.
    :return: DataFrame containing the data from the table.
    """
    engine = create_engine(connection_string)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, engine)
    return df


class EDA:
    def __init__(self, df: pd.DataFrame, filter_mostly_null: float = 1.0):
        """
        Initialize the EDA object with a DataFrame.
        :param df: dataframe to analyze
        :param filter_mostly_null: Threshold for filtering out mostly null columns.
        """
        self.df = df
        self.mostly_null_cols = self._filter_mostly_null(filter_mostly_null)
        self.df_filtered = self.df[[col for col in df.columns if col not in self.mostly_null_cols]]
        self._perform_eda()

    def count_nulls(self) -> pd.Series:
        """
        Count the number of null values in each column.
        """
        nc = self.df.isnull().sum().sort_values(ascending=False)
        nc.name = "null_count"
        return nc

    def _filter_mostly_null(self, threshold: float) -> List[str]:
        """
        Filter out columns with a high proportion of null values.
        :param threshold: Threshold for filtering out mostly null columns.
        :return: List of columns to keep.
        """
        return [col for col in self.df.columns if self.df[col].isnull().mean() < threshold]

    def _perform_eda(self, plots: bool = False) -> None:
        """
        Perform exploratory data analysis on the fetched data.
        """
        self.numerical_columns = self.df_filtered.select_dtypes(include=['int64', 'float64']).columns
        self.categorical_columns = self.df_filtered.select_dtypes(include=['object', 'string']).columns
        if plots:
            self.df_filtered[self.numerical_columns].dropna().hist()
            plt.title("Histogram of Numerical Columns")
            plt.show()
    @property
    def numerical(self):
        return self.df[self.numerical_columns]

    @property
    def categorical(self):
        return self.df[self.categorical_columns]

    def detect_outliers(self, column: str) -> pd.DataFrame:
        """
        Detect outliers in a numerical column using the Z-score method.
        :param column: Name of the numerical column to detect outliers for.
        :return: DataFrame with outliers marked as True.
        """
        if column not in self.numerical_columns:
            raise ValueError(f"{column} is not a numerical column.")
        z_scores = np.abs(stats.zscore(self.df_filtered[column]))
        return self.df_filtered[z_scores > 3]

    def perform_t_test(self, group1: str, group2: str) -> stats.ttest_ind:
        """
        Perform a t-test between two groups.
        :param group1: Name of the first group.
        :param group2: Name of the second group.
        :return: T-test results.
        """
        if group1 not in self.df_filtered.columns or group2 not in self.df_filtered.columns:
            raise ValueError(f"One or both of {group1} and {group2} are not in the DataFrame.")
        return stats.ttest_ind(self.df_filtered[group1], self.df_filtered[group2])

    def perform_anova_test(self, column: str, groups: List[str]) -> stats.f_oneway:
        """
        Perform an ANOVA test between multiple groups.
        :param column: Name of the numerical column to perform ANOVA on.
        :param groups: List of group names.
        :return: ANOVA results.
        """
        if column not in self.numerical_columns:
            raise ValueError(f"{column} is not a numerical column.")
        for group in groups:
            if group not in self.df_filtered.columns:
                raise ValueError(f"{group} is not in the DataFrame.")
        return stats.f_oneway(*[self.df_filtered[self.df_filtered[group] == g][column] for g in groups])

    def show_categorical_summary(self, column: str) -> pd.DataFrame:
        """
        Generate summary statistics for a categorical column.
        :param column: Name of the categorical column to generate summary statistics for.
        :return: Summary statistics DataFrame.
        """
        if column not in self.categorical_columns:
            raise ValueError(f"{column} is not a categorical column.")
        return pd.DataFrame({
            'Count': self.df_filtered[column].value_counts(),
            'Proportion': self.df_filtered[column].value_counts(normalize=True) * 100
        }).sort_values(by='Count', ascending=False)

    def plot_categorical(self, column: str, topn: int = 10) -> Optional[plt.Figure]:
        """
        Plot the categorical data.
        """
        try:
            assert column in self.categorical_columns
        except AssertionError:
            return f"{column} is not a categorical column."
        cats = self.show_categorical_summary(column)
        cats_top = cats.iloc[:topn]

        fig, ax = plt.subplots()
        cats_top['Proportion'].plot(kind='bar', ax=ax)
        if _not_in_ipython:
            return fig
