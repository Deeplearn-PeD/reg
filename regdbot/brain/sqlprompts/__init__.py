from regdbot.brain import dbtools as dbt
class PromptTemplate:
    """
    Class to generate Prompt templates for interactions with the OpenAI API
    for SQL query generation.   
    """
    def __init__(self, dialect: str = 'postgresql', db: str='duckdb:///:memory:') -> object:
        """
        Constructor for the PromptTemplate class
        :param dialect: SQL dialect to use in the query
        :param db: Database connection URL
        """
        self.db = db
        self.dialog = dialect
        self.system_preamble = f"""
        Given an input question about data in a relational database, 
        create a syntactically correct {dialect} query that will answer the question.
        
        You can use the following tables in your query:
        
        """
        self._prompt = None



    def add_table_description(self, table_name: str, description: str) -> None:
        for table in dbt.get_table_description(dbt.get_duckdb_connection(self.db), table_name):
            description += f"{table[0]}: {table[1]}\n"
            self.system_preamble += f"{table_name}: \n{description}"


    def get_prompt(self, question):
        if self._prompt is None:
            self._prompt = f"""
            {self.system_preamble}
            
            Question: {question}
            
            SQL Query:
            """
        return self._prompt