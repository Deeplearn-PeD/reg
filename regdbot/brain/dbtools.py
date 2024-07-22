from typing import List, Dict, Tuple, Any, Union
import dotenv
import os
import re
import sqlparse
import loguru
import duckdb
import sqlalchemy
import pandas as pd
from tabulate import tabulate
from sqlalchemy import create_engine, sql
from regdbot.brain.utils import extract_code_from_markdown
from duckdb.duckdb import InvalidInputException

dotenv.load_dotenv()
logger = loguru.logger


class Database:
    def __init__(self, dburl: str, llm: object) -> None:
        """
        Configure database connection for prompt generation
        :param dburl: any standard database url or csv:mycsv.csv for csv files
        :param llm: language model object
        """
        self.url = dburl
        self.llm = llm
        self._tables = []
        self._views = []
        self.table_descriptions = {}
        self.dialect = dburl.split(':')[
            0]  #'duckdb' if 'duckdb' in self.url.lower() else 'postgresql' if 'postgresql' in self.url.lower() else 'csv'
        self._connection = None
        self._tables = None

    @property
    def tables(self) -> List[str]:
        """
        Returns the list of tables in the database
        :return:
        """
        if not self._tables:
            if 'duckdb' in self.url:
                query = "SHOW TABLES;"
                result = self.connection.execute(query)
                self._tables = [row[0] for row in result.fetchall()]
                return self._tables
            elif 'postgresql' in self.url:
                query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
            elif 'csv' in self.url:
                query = f"show tables;"
                result = self.connection.execute(query)
                columns = [row[0] for row in result.fetchall()]
                return columns

            result = self.connection.execute(sql.text(query))
            self._tables = [row[0] for row in result.fetchall()]
        return self._tables

    @property
    def views(self) -> List[str]:
        """
        Returns the list of views in the database
        :return:
        """
        if not self._views:
            if 'duckdb' in self.url:
                query = "SHOW VIEWS;"
            elif 'postgresql' in self.url:
                query = "SELECT table_name FROM information_schema.views WHERE table_schema = 'public';"
            result = self.connection.execute(sql.text(query))
            self._views = [row[0] for row in result.fetchall()]

        return self._views

    @property
    def connection(self) -> Union[duckdb.DuckDBPyConnection, sqlalchemy.engine.Connection]:
        if self._connection is not None:
            return self._connection
        if 'duckdb' in self.url:
            return get_duckdb_connection(self.url)
        elif 'postgresql' in self.url:
            engine = create_engine(self.url)
            return engine.connect()
        elif 'csv':
            mdb = duckdb.connect()
            tname = os.path.split(self.url.split(':')[1])[1].split('.')[0]
            mdb.execute(f"CREATE TABLE {tname} AS SELECT * FROM '{self.url.split(':')[1]}';")
            return mdb
        else:
            logger.error(f"Database URL {self.url} not supported.")

    def get_table_description(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Returns the description of the table using duckdb
        :param table_name: name of the table
        :return:
        """
        if table_name in self.table_descriptions:
            return self.table_descriptions[table_name]
        if 'duckdb' in self.url:
            query = f"DESCRIBE SELECT * FROM {table_name};"
            result = self.connection.execute(query).fetchall()
        elif 'postgresql' in self.url:
            query = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}';"
            result = self.connection.execute(sql.text(query)).fetchall()
        elif 'csv' in self.url:
            result = self.connection.execute(f"DESCRIBE TABLE {self.tables[0]};").fetchall()
            # result = get_csv_description(self.url.split(":")[-1])
            # self.table_descriptions[table_name] = result
            # return result

        sample_rows = self._get_sample_rows(table_name)
        parsed_result = self._parse_table_description(result, sample_rows)
        self.table_descriptions[table_name] = parsed_result

        return parsed_result

    def _count_non_null_rows(self, table_name: str) -> List[int:]:
        pass

    def _get_sample_rows(self, table_name: str = '', num_rows: int = 5) -> List[Tuple[str, Any]]:
        """
        Returns a sample of rows from the table
        :param table_name: name of the table
        :param num_rows: number of rows to return
        :return: list of tuples
        """
        if table_name == '':
            table_name = self.tables[-1]
        if 'duckdb' in self.url:
            query = f"SELECT * FROM {table_name} LIMIT {num_rows};"
            result = self.connection.execute(query).fetchall()
        elif 'postgresql' in self.url:
            query = f"SELECT * FROM {table_name} LIMIT {num_rows};"
            result = self.connection.execute(sql.text(query)).fetchall()
        elif 'csv' in self.url:
            query = f"SELECT * FROM '{self.url.split(':')[1]}' LIMIT {num_rows};"
            return self.connection.execute(query).fetchall()

        return result

    def _parse_table_description(self, table_description: List, sample: List) -> str:
        """
        Parses the table description into a human-readable format
        :param table_description: description as generated by the database
        :param sample: sample rows from the table
        :return: human-readable table description
        """
        description = ""
        for n, column in enumerate(table_description):
            sample_values = f", sample values: {[r[n] for r in sample]}" if sample and n < len(sample[0]) else ""
            description += f"column name:{column[0]},  type:{column[1]}{sample_values}\n\n"
        return description

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
        view_name = view_name if view_name else f"{table_name}_semanticview"
        context = f"You will be asked to create SQL code in {self.dialect} dialect, to create a view with semantic " \
                  f"names for all the columns of a table. Be mindful of including only existing columns, as listed in the context. Do not use uppercase letters or spaces in the semantic column names." \
                  f"Don't use spaces, use underscores instead in variable names. Return pure and complete SQL clauses, which can be executed, without any accessory text." \
                  f"When you cannot propose a semantic name, maintain the original name\n"
        prompt = f"Generate a view of table {table_name}, named {view_name}  " \
                 "renaming column names with semantic names " \
                 f"including the columns described bellow:\\n{table_description}"


        code = self.llm.get_response(question=prompt, context=context)
        code = self.check_query(code, table_name)
        # parse the response to get the column descriptions
        column_descriptions = {}

        logger.info(f"Created semantic view {view_name} on table {table_name}")
        logger.info(f"using the following SQL code:\n{code}")
        # print(column_descriptions)
        return column_descriptions

    def check_query(self, query: str, table_name: str = None, debug_tries: int = 10) -> str:
        """
        Run a query through the database connection, debugging it if necessary
        :param query: SQL query to run
        :param table_name: Table name to run the query on
        :param debug_tries: number of times to try debugging the query
        :return:
        """
        # run the response through the duckdb connection to create the view
        if isinstance(query, str):
            sqlcode = self._clean_query_code(query)
        else:
            raise TypeError("Query must be a string")
        if table_name is None:
            table_name = self.tables[-1]
        tries = 0
        result = None
        while tries < debug_tries:
            if validate_sql(sqlcode):
                try:
                    if 'duckdb' in self.url:
                        result = self.connection.execute(sqlcode)
                    elif 'postgresql' in self.url:
                        result = self.connection.execute(sql.text(sqlcode))
                    break
                except Exception as e:
                    logger.error(f"{e} Error running query: {sqlcode[:100]},\n debugging the code")
                    sqlcode = self.debug_query(sqlcode, table_name)
                    sqlcode = extract_code_from_markdown(sqlcode)
                    tries += 1
            else:
                logger.error(f"SQL syntax error in query: {sqlcode[:100]}")
                break
        return sqlcode

    def debug_query(self, query: str, table_name: str) -> List[Tuple[str, Any]]:
        """
        Debug a query by running it through the database connection
        :param query: SQL query to run
        :return: result of the query
        """

        question = (
            f"Given the following defective SQL query of table {table_name}, please fix its bugs and return a working version" \
            f"Return pure, complete SQL code without explanatory text:\n\n{query}")
        # print(self.table_descriptions[table_name])
        response = self.llm.get_response(question, self.table_descriptions[table_name])
        # response = self._clean_query_code(response)
        clean_response = extract_code_from_markdown(response)
        new_code = clean_response if isinstance(clean_response, str) else clean_response['response']
        new_code = extract_code_from_markdown(new_code)
        return new_code

    def _clean_query_code(self, query: str) -> str:
        """
        Clear the query code from any non-SQL code using regular expressions
        :param query: SQL query to clear
        :return: cleaned SQL query
        """
        # Remove "```sql" and "sql```" tags
        sql_code = re.sub(r'```sql|sql```', '', query)
        # remove any remaining backticks
        sql_code = re.sub(r'```', '', sql_code)

        # Remove leading and trailing whitespace
        sql_code = sql_code.lstrip('sql')
        sql_code = sql_code.strip()

        # Remove whitespace and newlines
        sql_code = re.sub(r'\s+', ' ', sql_code)
        sql_code = re.sub(r'\n+', '', sql_code)

        return sql_code

    def run_query(self, query: str) -> Tuple[List[Tuple[str, Any]], List[str]]:
        """
        Run a query through the database connection
        :param query: SQL query to run
        :return: result of the query
        """
        if isinstance(query, str):
            sqlcode = query.split("```sql")[1].strip("```").strip() if '```sql' in query else query.strip()
        else:
            raise TypeError("Query must be a string")
        if 'duckdb' in self.url:
            result = self.connection.execute(sqlcode)
        elif 'postgresql' in self.url:
            result = self.connection.execute(sql.text(sqlcode))
        elif 'csv' in self.url:
            result = self.connection.execute(sqlcode)
        # print(sqlcode)
        try:
            return result.fetchall(), result.keys()
        except InvalidInputException as e:
            print(e)
            return [], []

    def get_table_df(self, table_name: str) -> object:
        """
        Returns a pandas dataframe from the table
        :param table_name: name of the table
        :return: pandas dataframe
        """
        if 'duckdb' in self.url:
            query = f"SELECT * FROM {table_name};"
            result = self.connection.execute(query).df()
            return result
        elif 'postgresql' in self.url:
            query = f"SELECT * FROM {table_name};"
            df = pd.read_sql_query(query, self.connection)
            return df
        elif 'csv' in self.url:
            query = f"SELECT * FROM '{self.url.split(':')[1]}';"
            return self.connection.execute(query).df()



def get_duckdb_connection(url: str) -> object:
    """
    Returns a connection to a duckdb database
    :param url: URL to the duckdb database
    :return: duckdb connection object
    """
    if url == 'duckdb:///:memory:':
        return duckdb.connect()
    else:  # for persistent databases
        pth = url.split("://")[1]
        return duckdb.connect(pth)


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




def validate_sql(query):
    try:
        sqlparse.parse(query)
        return True
    except sqlparse.exceptions.SQLParseError:
        return False
