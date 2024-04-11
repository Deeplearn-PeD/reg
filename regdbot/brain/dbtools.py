from typing import List, Dict, Tuple, Any, Union
import dotenv
import os
import ollama
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
        self._tables = []

    @property
    def tables(self) -> List[str]:
        """
        Returns the list of tables in the database
        :return:
        """
        if not self._tables:
            if 'duckdb' in self.url:
                query = "SHOW TABLES;"
            elif 'postgresql' in self.url:
                query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
            elif 'csv' in self.url:
                query = f"DESCRIBE TABLE '{self.url.split(':')[1]}';"
            result = self.connection.execute(sql.text(query))
            self._tables = [row[0] for row in result.fetchall()]
        return self._tables



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

    def _create_semantic_view(self, table_name: str, view_name: str = None, duckdb_view: bool = False) -> None:
        """
        Creates a view in the database with semantic renaming of the columns for enhanced readability
        :param table_name: table name in the database to create the view on
        :param view_name: view name. if not given will default to table_name_semanticview
        :duckdb_view: if True, will create an in memory duckdb view instead of a sql view
        """
        # get current table description
        table_description = self.get_table_description(table_name)
        # Prompt gemma model through ollama to generate SQL code with semantic naming for the view
        response = ollama.generate(
            model="gemma",
            system=f"You will be asked to create SQL code in {self.dialect} dialect, to create a view with semantic "
                   f"names for the columns of a table.",
            prompt=f"Generate SQL code with semantic names for the columns of table {table_name}\n",
        )
        # run the response through the duckdb connection to create the view
        self.connection.execute(sql.text(response['response']))
        # parse the response to get the column descriptions
        column_descriptions = {}
        for line in response.text.split("\n"):
            if line.startswith("Column"):
                column_name = line.split(":")[1].strip()
            elif line.startswith("Description"):
                description = line.split(":")[1].strip()
                column_descriptions[column_name] = description

        logger.info(f"Created semantic view {view_name} on table {table_name}")
        logger.info(f"using the following SQL code:\n{response['response']}")
        print(column_descriptions)
        return column_descriptions




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