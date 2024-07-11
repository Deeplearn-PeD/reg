'''
Data ingestion code
'''
import pandas as pd
from deltalake import DeltaTable, write_deltalake
from sqlalchemy import create_engine

from regdbot.brain.dbtools import get_duckdb_connection


class CSVIngestor:
    """
    A class to ingest CSV data and write it to a Delta table.

    Attributes:
        file_path (str): The path to the CSV file to be ingested.
        data (pd.DataFrame): The pandas DataFrame holding the ingested data. Initially None until `ingest` is called.

    Methods:
        ingest(): Reads the CSV file into a pandas DataFrame.
        to_delta(path: str): Writes the ingested data to a Delta table at the specified path.
    """

    def __init__(self, file_path: str, table_name: str = None):
        """
        Initializes the CSVIngestor with the specified file path.
        :param file_path:
        :param table_name: Name of the table to use when creating a Delta table, or database table. if not given, default to the file name without extension.
        """
        self.table_name = table_name if table_name else file_path.split('/')[-1].split('.')[
            0]  # Default table name is file name without extension
        self.data = None
        self.file_path = file_path
        self.delta_lake = None
        self.delta_lake_path = None
        self.data = None
        self.ingest()

    def ingest(self) -> pd.DataFrame:
        """
        Reads the CSV file into a pandas DataFrame.

        Returns:
            pd.DataFrame: The ingested data as a pandas DataFrame.
        """
        if self.data is None:
            self.data = pd.read_csv(self.file_path)
        else:
            self.data = pd.read_csv(self.file_path)
        return self.data

    def to_delta(self, path: str = None) -> DeltaTable:
        """
        Writes the ingested data to a Delta table at the specified path.

        Parameters:
            path (str): The path where the Delta table will be written.

        Returns:
            str: The path where the Delta table was written.
        """
        if path is None:
            path = f'delta/{self.table_name}'
        write_deltalake(path, self.data, mode='overwrite')
        self.delta_lake = DeltaTable(path)
        self.delta_lake_path = path
        return self.delta_lake

    def to_database(self, dburl: str) -> None:
        """
        Writes the ingested data to a database.

        Parameters:
            dburl (str): The URL for the database connection.
        """
        if dburl.startswith('duckdb'):
            conn = get_duckdb_connection(dburl)
            conn.execute(f"CREATE TABLE {self.table_name} AS SELECT * FROM delta_scan('{self.delta_lake_path}')")
        else:
            engine = create_engine(dburl)
            conn = engine.connect()
        conn.commit()

        conn.close()
