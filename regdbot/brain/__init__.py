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
        You are a database engineer. When asked a question about a database, 
        you should provide a SQL query that answers the question. do not provide 
        answers that are not based on the database specified
        Given an input question about data in a relational database table, 
        create a syntactically correct SQL query that will answer the question.
        Write your answers in Markdown, with any SQL code inside markdown code blocks.

        """,
                   'pt_BR': f"""
        Você é um engenheiro de banco de dados. Quando perguntado sobre um banco de dados, 
        você deve fornecer uma consulta SQL que responda à pergunta. Não forneça
        respostas que não se baseiem no banco de dados especificado.
        Dada uma pergunta de entrada sobre dados em uma tabela de um banco de dados relacional,
        crie uma consulta SQL sintaticamente correta que responderá à pergunta.
        Escreva suas respostas em Markdown, com quaisquer blocos de código SQL marcados como código.
        
        """
                   }


class RegDBot(Persona):
    def __init__(self, name: str = 'Reggie D. Bot', model: str = 'gpt-4o'):
        super().__init__(name=name, model=model)
        self.llm = LangModel(model=model)
        self.context_prompt: str = system_preamble[self.active_language]
        self.active_db = None
        self.last_response = {}

    def load_database(self, dburl: str):
        """
        Load the database connection for prompt generation
        :param dburl: URL for the database connection
        :param dialect: kind of SQL dialect to use
        """
        self.active_db = dbt.Database(dburl, self.llm)
        for tbl in self.active_db.tables:
            self.active_db.get_table_description(tbl)
        self.context_prompt += f"\nYou are analyzing a {self.active_db.dialect} database\n{system_preamble[self.active_language]}.\n{self.active_db.tables}"

    @property
    def context(self):
        return self.context_prompt

    def set_context(self, context: str=None) -> None:
        """
        Set the context for the bot's response
        :param context: text
        """
        if context is None:
            self.context_prompt = system_preamble[self.active_language]
        else:
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
            question_plus = question + f"\n\nPlease take into account this description of the table:\n {self.active_db.table_descriptions[table]}"
        response = self.get_response(question_plus)
        preamble, query, explanation = self._parse_response(response)
        if not query.strip(): # agent response does not contain a query
            return response
        if self.active_db is not None:
            query = self.active_db.check_query(query.strip('\n'), table)
            result = self.active_db.run_query(query)
            if len(result):
                result = self._prettify_results(table, query, result)
        answer = f"{preamble}\n\n```sql\n{query}\n```\n\nWhich gives this result:\n\n{result}\n\n{explanation}"
        return answer

    def _parse_response(self, response: str) -> tuple[str, str, str]:
        """
        Parse the response from the language model  into preamble, query, and explanation
        trying to detect when there is a mix of code and text in the response.
        :param response: Raw llm response
        :return: tuple of preamble, query, explanation
        """

        parts = response.split('```sql') if '```sql' in response else response.split('```') if '```sql' in response else response.split('`')
        if len(parts) > 1:
            preamble = parts[0]
            if len(parts) > 2:
                query, explanation = parts[1],parts[2]
            else:
                query, explanation = parts[1].split('```')
        else: # no code block in response
            preamble = response
            query, explanation = ('', '')
        self.last_response = {'preamble': preamble, 'query': query.strip(), 'explanation': explanation}
        return preamble, query.strip(), explanation

    def get_response(self, question):
        response = self.llm.get_response(question=question, context=self.context_prompt)
        return response

    def _prettify_results(self, table: str, query: str, results: str):
        """
        Ask LLM to teke the return value of a query and format it maximizing user readability
        :param table: table name
        :param query: SQL query
        :param results: results of the query
        """
        self.set_context(f"""
You are a helpful data analyst. Given the output of a query on a table named {table}, you should reformat the output below to make it more readable.

{results} 
        """)
        response = self.get_response(f"The query below and its results are not very readable. Please reformat the results to make them more user-friendly as a markdown text.\n\nQuery:\n{query}\n\nResults:\n{results}")
        self.set_context()
        return response


    def get_prompt(self):
        return self.context_prompt
