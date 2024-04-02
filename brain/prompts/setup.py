import openai
from brain import dbtools as dbt


class PromptTemplate:
    """
    Class to generate Prompt templates for interactions with the OpenAI API
    for SQL query generation.
    """
    def __init__(self, prompt, dialect='postgresql'):
        self.system_preamble = f"""
        Given an input question about data in a relational database, 
        create a syntactically correct {dialect} query that will answer the question.
        
        You can use the following tables in your query:
        
        """
        self.prompt = prompt


    def add_table_description(self, table_name, description):
        self.system_preamble += f"{table_name}: \n{description}"
    def generate_code(self):
        code = f"""
        """
