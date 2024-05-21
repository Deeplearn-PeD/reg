"""
in This package we define the Bot's Brain, i.e. its professional profile.
What it knows, how it learns,
how it should interact with the user, and how it should respond to the user's requests.
"""
from regdbot import Persona
from base_agent.llminterface import LangModel
from regdbot.brain import dbtools as dbt
import dotenv
import os

dotenv.load_dotenv()

system_preamble = {'en_US': f"""
        Given an input question about data in a relational database, 
        create a syntactically correct query that will answer the question.
        
        You can use the following tables in your query:
        
        """,
                   'pt_BR': f"""
        Dada uma pergunta de entrada sobre dados em um banco de dados relacional,
        crie uma consulta sintaticamente correta que responderá à pergunta.
        
        Você pode usar as seguintes tabelas em sua consulta:
        
        """
                   }


class RegDBot(Persona):
    def __init__(self, name: str = 'Reggie D. Bot', model: str = 'gpt-4-0125-preview'):
        super().__init__(name=name, model=model)
        self.llm = LangModel(model=model)
        self.context_prompt: str = system_preamble[self.active_language]
        self.active_db = None

    def load_database(self, dburl: str):
        """
        Load the database connection for prompt generation
        :param dburl: URL for the database connection
        :param dialect: kind of SQL dialect to use
        """
        self.active_db = dbt.Database(dburl)
        for tbl in self.active_db.tables:
            self.active_db.get_table_description(tbl)
        self.context_prompt += f"\nYou are analyzing a {self.active_db.dialect} database\n{system_preamble[self.active_language]}.\n{self.active_db.tables}"

    @property
    def context(self):
        return self.context_prompt

    def set_context(self, context: str) -> None:
        self.context_prompt = context

    def set_prompt(self, prompt_template):
        self.prompt_template = prompt_template

    def ask(self, question: str, table: str = None):
        """
        Ask the bot a question about a table in the database.
        :param question: Question to ask the bot about the specified table
        :param table: Table to query before generating the response
        :return:
        """
        if table is None:
            question_plus = question
        else:
            question_plus = question + f"\nPlease take into acount this description of the table:\n {self.active_db.table_descriptions[table]}"
        response = self.get_response(question_plus)
        preamble, query, explanation = self._parse_response(response)
        if self.active_db is not None:
            query = self.active_db.check_query(query.strip('\n'), table)
            result = self.active_db.run_query(query)
        answer = f"{preamble}\n\n{query}\n\n{result}"
        return answer

    def _parse_response(self, response: str) -> tuple[str, str, str]:
        """
        Parse the response from the language model  into preamble, query, and explanation
        trying to detect when there is a mix of code and text in the response.
        :param response: Raw llm response
        :return:
        """
        if '```' in response:
            preamble = response.split('```sql')[0]
            query = response.split('```sql')[-1].split('```')[0]
            explanation = response.split('```sql')[-1].split('```')[-1]
        else:
            preamble = ''
            query = response.strip()
            explanation = ''
        return preamble, query, explanation

    def get_response(self, question):
        response = self.llm.get_response(question=question, context=self.context_prompt)
        return response

    def get_prompt(self):
        return self.context_prompt
