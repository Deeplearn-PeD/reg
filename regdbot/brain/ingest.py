'''
Data ingestion code
'''
import pandas as pd
import duckdb
from deltalake import DeltaTable, write_deltalake


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
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.delta_lake = None
        self.delta_lake_path = None
        self.data = None

    def ingest(self) -> pd.DataFrame:
        """
        Reads the CSV file into a pandas DataFrame.

        Returns:
            pd.DataFrame: The ingested data as a pandas DataFrame.
        """
        self.data = pd.read_csv(self.file_path)
        return self.data

    def to_delta(self, path: str) -> DeltaTable:
        """
        Writes the ingested data to a Delta table at the specified path.

        Parameters:
            path (str): The path where the Delta table will be written.

        Returns:
            str: The path where the Delta table was written.
        """
        write_deltalake(path, self.data,  mode='overwrite')
        self.delta_lake = DeltaTable(path)
        self.delta_lake_path = path
        return self.delta_lake