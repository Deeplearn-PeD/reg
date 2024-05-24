"""
This module contains functions for analyzing data from the database.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

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

def perform_eda(df):
    """
    Perform exploratory data analysis on the fetched data.
    :param df: DataFrame containing the data from the table.
    """
    # Print basic statistics
    print(df.describe(include='all'))

    # Check for missing values
    print("\nMissing values:")
    print(df.isnull().sum())

    # Plot histograms for numerical columns
    numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns

    df[numerical_columns].dropna().hist()
    plt.title(f"Histogram of Numerical Columns")
    plt.show()

    # Correlation analysis
    print("\nCorrelation Matrix:")
    corr_matrix = df[numerical_columns].dropna().corr()
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", linewidths=.5)
    plt.title("Correlation Heatmap")
    plt.show()

    # Describe categorical variables
    categorical_columns = df.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        print(f"\n{col}:")
        print(df[col].value_counts(normalize=True) * 100)
        plt.figure()
        sns.countplot(x=col, data=df)
        plt.title(f"Count Plot of {col}")
        plt.xlabel(col)
        plt.ylabel("Percentage")
        plt.xticks(rotation=45)
        plt.show()

# Example usage:
# df = get_data_from_db('your_table_name', 'your_connection_string')
# perform_eda(df)