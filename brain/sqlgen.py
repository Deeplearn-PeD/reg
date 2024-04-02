from typing import List, Dict, Tuple, Any
import dotenv
import os
import loguru
import duckdb
from sqlalchemy import create_engine

dotenv.load_dotenv()
logger = loguru.logger


def get_db_url(connvar: str = 'PGURL') -> str:
    """
    Returns the database connection url
    as defined in the environment variable `conn` 
    :param connvar: Environment variable containing the database connection URL
    :return: URL to database connection
    """
    return os.getenv(connvar)


def get_db(connvar='PGURL') -> object:
    """
    Returns the database connection object
    :return:
    """
    engine = create_engine(get_db_url(connvar=connvar))
    return engine

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


def get_table_description(engine, table_name: str) -> List[Dict[str, Any]]:
    """
    Returns the description of the table using duckdb
    :param engine:
    :param table_name:
    :return:
    """
    query = f"DESCRIBE SELECT * FROM {table_name};"
    if isinstance(engine, duckdb.duckdb.DuckDBPyConnection):
        result = engine.execute(query)
    else:
        with engine.connect() as conn:
            result = conn.execute(query)

    return result.fetchall()

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