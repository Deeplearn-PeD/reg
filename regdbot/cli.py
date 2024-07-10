import os
import fire
from regdbot.brain import RegDBot
from base_agent.voice import talk
from regdbot.brain import statements
from regdbot.brain.utils import extract_code_from_markdown
from regdbot import config
import dotenv
import json
import pprint as pp

dotenv.load_dotenv()


class Reggie:
    def __init__(self, model='codellama', language: str = config["languages"]["English"]["code"]):
        self.bot = RegDBot(model=model)
        self.bot.set_language(language)

    def say(self, text):
        self.bot.say(text)

    def ask(self, question: str, table: str) -> str:
        """
        Ask Reggie a question.
        :param question: any textual prompt
        :param table: the table name
        :return:
        """
        return self.bot.ask(question, table)

    def auto(self, db: str):
        """
        Execute query automatically just through the CLI
        :param db: database url
        """
        self._load_db(db)

        print("Please wait while I gather information about the database...")
        description = self.bot.get_response(f"Given the list of table names below, please generate a JSON object with "
                                            f"one-sentence descriptions for each table's content based on their name. "
                                            f"\n\n{self.bot.active_db.tables}")
        description = json.loads(extract_code_from_markdown(description).strip())
        print(f"The database specified contain the following tables\n\n")
        pp.pprint(description)
        while True:
            tbl_name = input("Please name one to query:")
            if tbl_name.strip() in description:
                break
            else:
                print("Table name not found in the list. Please try again.")
        self.bot.active_db.get_table_description(tbl_name.strip())

        question = input("What do you want to know?")
        self.bot.llm._set_active_model('codellama')
        print(self.ask(question, tbl_name))

    def _load_db(self, db):
        if 'postgresql' in db:
            self.bot.load_database(db)
        elif 'duckdb' in db:
            self.bot.load_database(db)
        elif 'csv' in db:
            self.bot.load_database(db)

    def introduction(self):
        for line in talk.introductions[self.bot.active_language]:
            self.say(line)
        self.bot.active_db.get_db_info()

    def info(self, dbtype: str):
        """
        Get information about the database
        :param dbtype: postgresql or duckdb or csv
        """
        self.say(statements.db_questions[self.bot.active_language][1])
        self.say('OK!')
        self._load_db(dbtype)
        if dbtype.startswith('csv'):
            self.say('This is a CSV file')
            self.say('It contains the following columns:')
            pp.pprint(self.bot.active_db.tables)
            description = self.bot.active_db.get_table_description('csv')
            self.say('What do you want to know about this data?')
            question = input("What do you want to know about this data?")
            resp = self.ask(question, 'csv')
        else:
            for q in statements.table_list[self.bot.active_language]:
                self.say(q)
            pp.pprint(self.bot.active_db.tables)
            for s in statements.table_questions[self.bot.active_language]:
                self.say(s)
            while True:
                tbl_name = input("Please name one to query:")
                if tbl_name.strip() in self.bot.active_db.tables:
                    break
                else:
                    print("Table name not found in the list. Please try again.")
            description = self.bot.active_db.get_table_description(tbl_name.strip())
            self.say(description)


def main():
    reggie = Reggie(model='llama3', language='en_US')
    fire.Fire(reggie)
