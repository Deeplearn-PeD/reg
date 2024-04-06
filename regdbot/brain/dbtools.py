from typing import List, Dict, Tuple, Any, Union
import dotenv
import os
import loguru
import duckdb
import sqlalchemy
from sqlalchemy import create_engine, sql


dotenv.load_dotenv()
logger = loguru.logger


class Database:
    def __init__(self, dburl) -> None:
        """
        Configure database connection for prompt generation
        :param dburl: any standard database url or csv:mycsv.csv for csv files
        """
        self.url = dburl

    @property
    def connection(self) -> Union[duckdb.DuckDBPyConnection, sqlalchemy.engine.Connection]:
        if 'duckdb' in self.url:
            return get_duckdb_connection(self.url)
        elif 'postgresql' in self.url:
            engine = create_engine(self.url)
            return engine.connect()
        elif 'csv':
            mdb = duckdb.connect()
            mdb.execute(f'select * from {self.url.split(":")[1]}')
            return mdb
        else:
            logger.error(f"Database URL {self.url} not supported.")

    def get_table_description(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Returns the description of the table using duckdb
        :param table_name:
        :return:
        """
        if 'duckdb' in self.url:
            query = f"DESCRIBE SELECT * FROM {table_name};"
        elif 'postgresql' in self.url:
            query = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}';"
        elif 'csv' in self.url:
            result = get_csv_description(self.url)
            return result
        result = self.connection.execute(sql.text(query))

        return result.fetchall()




def get_duckdb_connection(url: str) -> object:
    """
    Returns a connection to a duckdb database
    :param url: URL to the duckdb database
    :return: duckdb connection object
    """
    if url == 'duckdb:///:memory:':
        return duckdb.connect()
    else: # for persistent databases
        return duckdb.connect(url)




def get_csv_description(file_path: str) -> List[Tuple[str, Any]]:
    """
    Returns the description of the csv file using duckdb
    :param file_path: file path or URL for remote file
    :return: list of tuples
    """
    mdb = duckdb.connect()
    query = f"DESCRIBE TABLE '{file_path}';"
    result = mdb.execute(query).fetchall()
    return result