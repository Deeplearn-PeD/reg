"""
This module contains functions for analyzing data from the database.
"""
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine

try:
    __IPYTHON__
    _not_in_ipython = False
except NameError:
    _not_in_ipython = True
    matplotlib.use("svg")


def get_data_from_db(table_name, connection_string):
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
    def __init__(self, df, filter_mostly_null=1.0):
        """
        Initialize the EDA object with a DataFrame.
        :param df: dataframe to analyze
        :param filter_mostly_null: Threshold for filtering out mostly null columns.
        """
        self.df = df
        self.df_filtered = None  # Filtered DataFrame with mostly null columns removed
        self.mostly_null_cols = self._filter_mostly_null(filter_mostly_null)
        self._perform_eda()

    def count_nulls(self):
        """
        Count the number of null values in each column.
        """
        nc = self.df.isnull().sum().sort_values(ascending=False)
        nc.name = "null_count"
        return nc

    def _filter_mostly_null(self, threshold: float = 0.9) -> list:
        """
        Filter out columns that are mostly null based on a threshold.
        """
        null_counts = self.count_nulls()
        total_rows = len(self.df)
        self.complete_cols = null_counts[null_counts == 0].index
        mostly_null_cols = null_counts[null_counts / total_rows > threshold].index
        # Perform type inference and conversion
        self.df = self.df.infer_objects().convert_dtypes()
        # Drop mostly null columns
        self.df_filtered = self.df.drop(columns=mostly_null_cols)
        return mostly_null_cols

    def describe(self, include=None):
        """
        Generate a description of the data.
        """
        return self.df.describe(include=include)

    def plot_correlation(self):
        """
        Plot the correlation matrix of the numerical columns.
        """
        fig, ax = plt.subplots()
        corr_matrix = self.df_filtered[self.numerical_columns].dropna().corr()
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", linewidths=.5, ax=ax)
        plt.title("Correlation Heatmap")
        if _not_in_ipython:
            return fig

    def show_categorical(self, column=None):
        """
        Describe the categorical columns in the data.
        """
        if column is None:
            column = self.categorical_columns[0]
        try:
            counts = pd.merge(left=self.df_filtered[column].value_counts(),
                              right=self.df_filtered[column].value_counts(normalize=True) * 100,
                              on=column)
            assert column in self.categorical_columns
        except AssertionError:
            return f"{column} is not a categorical column."
        except KeyError:
            return f"{column} not found in the DataFrame"
        return counts.sort_values(by="proportion", ascending=False)

    def plot_categorical(self, column, topn=10):
        """
        Plot the categorical data.
        """
        try:
            assert column in self.categorical_columns
        except AssertionError:
            return f"{column} is not a categorical column."
        except KeyError:
            return f"{column} not found in the DataFrame"
        cats = self.show_categorical(column)
        cats_top = cats.iloc[:topn]

        fig, ax = plt.subplots()
        cats_top.proportion.plot(kind='bar', ax=ax)
        if _not_in_ipython:
            return fig
    def _perform_eda(self, plots=False):
        """
        Perform exploratory data analysis on the fetched data.
        """
        self.numerical_columns = self.df_filtered.select_dtypes(include=['int64', 'float64']).columns
        self.categorical_columns = self.df_filtered.select_dtypes(include=['object', 'string']).columns
        if plots:
            self.df_filtered[self.numerical_columns].dropna().hist()
            plt.title("Histogram of Numerical Columns")
            plt.show()

        # Describe categorical variables
        # categorical_columns = self.df.select_dtypes(include=['object']).columns
        # pprint(categorical_columns)
        # if plots:
        #     for col in categorical_columns:
        #         print(f"\n{col}:")
        #         print(self.df[col].value_counts(normalize=True) * 100)
        #         plt.figure()
        #         sns.countplot(x=col, data=self.df)
        #         plt.title(f"Count Plot of {col}")
        #         plt.xlabel(col)
        #         plt.ylabel("Percentage")
        #         plt.xticks(rotation=45)
        #         plt.show()

# Example usage:
# df = get_data_from_db('your_table_name', 'your_connection_string')
# perform_eda(df)
