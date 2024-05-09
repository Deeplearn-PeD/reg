import os
from typing import List, Tuple, Dict, Union, Any
import fire
from regdbot.brain import RegDBot
from base_agent.voice import talk
from regdbot.brain import statements
import dotenv
import json
import pprint as pp

dotenv.load_dotenv()


class Reggie:
    def __init__(self, model='gemma', language: str = 'pt_BR'):
        self.bot = RegDBot(model=model)
        self.bot.set_language(language)

    def say(self, text):
        self.bot.say(text)

    def ask(self, question, table: str = None):
        """
        Ask Reggie a question.
        :param question: any textual prompt
        :return:
        """
        return self.bot.ask(question, table)

    # def prepare_db(self, db: str, tables: Tuple[str] = None):
    #     """
    #     Prepare a database for querying
    #     :param db: database url
    #     :param tables: table name or tuple of names
    #     """
    #
    #     tables = prompt.db.tables if tables is None else tables
    #     for table in sorted(tables):
    #         print(table)
    #         description = input(f"Entre uma descrição para tabela {table} ou <enter>:")
    #         prompt.db._create_semantic_view(table)
    #         prompt.add_table_description(table, description)
    #
    #     self.bot.set_prompt(prompt)

    def auto(self, db: str):
        """
        Execute query automatically just through the CLI
        :param db: database url
        :param tables: table name or tuple of names
        """
        self.bot.load_database(os.getenv('PGURL') if 'postgresql' in db else os.getenv('DUCKURL'), dialect=db)
        tbl_desc = {}
        print("Please wait while I gather information about the database...")
        description = self.bot.get_response(f"Given the list of table names below, please generate a JSON object with "
                                            f"one-sentence descriptions for each table's content based on their name. \n\n{self.bot.active_db.tables}")
        description = json.loads(description.split('```json')[1].split('```')[0].strip())
        print(f"The database specified contain the following tables\n\n")
        pp.pprint(description)
        while True:
            tbl_name = input("Please name one to query:")
            if tbl_name in description:
                break
            else:
                print("Table name not found in the list. Please try again.")
        self.bot.active_db.get_table_description(tbl_name)

        question = input("What do you want to know?")
        print(self.ask(question, tbl_name))

    def introduction(self):
        for line in talk.introductions[self.bot.active_language]:
            self.say(line)
        self.get_db_info()

    def info(self, dbtype: str):
        """
        Get information about the database
        :param dbtype: postgresql or duckdb or csv
        """
        self.say(statements.db_questions[self.bot.active_language][1])
        self.say('OK!')
        self.bot.load_database(os.getenv('PGURL') if dbtype == 'postgresql' else os.getenv('DUCKURL'), dialect=dbtype)


        for q in statements.table_questions[self.bot.active_language]:
            self.say(q)



def main():
    reggie = Reggie(model='wizard', language=os.environ.get('LANGUAGE', 'en_US'))
    fire.Fire(reggie)
