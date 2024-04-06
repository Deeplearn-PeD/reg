import os

import fire
from regdbot.brain import RegDBot
from regdbot.brain.sqlprompts import PromptTemplate
from regdbot.voice import talk
import dotenv

dotenv.load_dotenv()


class Reggie:
    def __init__(self, language: str='pt_BR'):
        self.bot = RegDBot()
        self.bot.set_language(language)


    def say(self, text):
        self.bot.say(text)

    def ask(self, question):
        return self.bot.ask(question)

    def introduction(self):
        for line in talk.introductions[self.bot.active_language]:
            self.say(line)
        self.get_db_info()

    def get_db_info(self):

        self.say(talk.db_questions[self.bot.active_language][0])
        dbtype = input('Escolha postgresql, duckdb ou csv:')
        self.say(talk.db_questions[self.bot.active_language][1])
        self.say('OK!')

        prompt = PromptTemplate(os.getenv('PGURL') if dbtype == 'postgresql' else os.getenv('DUCKURL'))
        for q in talk.table_questions[self.bot.active_language]:
            self.say(q)
        table_names = input('Nome(s):')
        table_names = table_names.split(',')
        for table_name in table_names:
            prompt.add_table_description(table_name, '')




def main():
    reggie = Reggie()
    fire.Fire(reggie)