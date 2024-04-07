from regdbot.brain import dbtools as dbt
class PromptTemplate:
    """
    Class to generate Prompt templates for interactions with the OpenAI API
    for SQL query generation.   
    """
    def __init__(self, dburl:str, dialect: str = 'postgresql', language='pt_BR') -> object:
        """
        Constructor for the PromptTemplate class
        :param dialect: SQL dialect to use in the query
        :param db: Database connection URL
        """
        self.db = dbt.Database(dburl)
        self.language = language
        self.dialog = dialect
        self.system_preamble = {'en_US': f"""
        Given an input question about data in a relational database, 
        create a syntactically correct {dialect} query that will answer the question.
        
        You can use the following tables in your query:
        
        """,
        'pt_BR': f"""
        Dada uma pergunta de entrada sobre dados em um banco de dados relacional,
        crie uma consulta {dialect} sintaticamente correta que responderá à pergunta.
        
        Você pode usar as seguintes tabelas em sua consulta:
        
        """
        }

        self._prompt = None



    def add_table_description(self, table_name: str, description: str) -> None:
        for table in self.db.get_table_description(table_name):
            description += f"{table[0]}: {table[1]}\n"
            self.system_preamble[self.language] += f"{table_name}: \n{description}"


    def get_prompt(self):
        if self._prompt is None:
            self._prompt = self.system_preamble[self.language]
            return self._prompt