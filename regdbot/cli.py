import os
from typing import List, Tuple, Dict, Union, Any
import fire
from regdbot.brain import RegDBot
from regdbot.brain.sqlprompts import PromptTemplate
from base_agent.voice import talk
import dotenv

dotenv.load_dotenv()


class Reggie:
    def __init__(self, model='gemma', language: str = 'pt_BR'):
        self.bot = RegDBot(model=model)
        self.bot.set_language(language)

    def say(self, text):
        self.bot.say(text)

    def ask(self, question):
        """
        Ask Reggie a question.
        :param question: any textual prompt
        :return:
        """
        return self.bot.ask(question)

    def prepare_db(self, db: str, tables: Tuple[str] = None):
        """
        Prepare a database for querying
        :param db: database url
        :param tables: table name or tuple of names
        """
        prompt = PromptTemplate(os.getenv('PGURL') if 'postgresql' in db else os.getenv('DUCKURL'),
                                language=self.bot.active_language)
        tables = prompt.db.tables if tables is None else tables
        for table in sorted(tables):
            print(table)
            description = input(f"Entre uma descrição para tabela {table} ou <enter>:")
            prompt.db._create_semantic_view(table)
            prompt.add_table_description(table, description)

        self.bot.set_prompt(prompt)

    def auto(self, db: str, tables: Tuple[str]):
        """
        Execute query automatically just through the CLI
        :param db: database url
        :param tables: table name or tuple of names
        """
        prompt = PromptTemplate(os.getenv('PGURL') if 'postgresql' in db else os.getenv('DUCKURL'),
                                language=self.bot.active_language)
        for table in tables:
            description = input(f"Entre uma descrição para tabela {table} ou <enter>:")
            prompt.add_table_description(table, description)

        self.bot.set_prompt(prompt)
        print("Approximate # of tokens in context: ",
              len(self.bot.prompt_template.system_preamble[self.bot.active_language
                  ][:2048].split()))
        # print(self.bot.prompt_template.system_preamble)
        question = input("O que você deseja saber?")
        print(self.ask(question))

    def introduction(self):
        for line in talk.introductions[self.bot.active_language]:
            self.say(line)
        self.get_db_info()

    def get_db_info(self):

        self.say(talk.db_questions[self.bot.active_language][0])
        dbtype = input('Escolha postgresql, duckdb ou csv:')
        self.say(talk.db_questions[self.bot.active_language][1])
        self.say('OK!')

        prompt = PromptTemplate(os.getenv('PGURL') if dbtype == 'postgresql' else os.getenv('DUCKURL'),
                                language=self.bot.active_language)

        for q in talk.table_questions[self.bot.active_language]:
            self.say(q)
        table_names = input('Nome(s):')
        table_names = table_names.split(',')
        for table_name in table_names:
            prompt.add_table_description(table_name, '')
        self.bot.set_prompt(prompt)


def main():
    reggie = Reggie(model='llama')
    fire.Fire(reggie)
