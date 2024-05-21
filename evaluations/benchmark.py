import json
import os
# from braintrust import Eval
# from autoevals import Factuality
from regdbot.brain import RegDBot
from regdbot import config
import dotenv

dotenv.load_dotenv()


class ApplyEvaluation:
    def __init__(self, dburl="duckdb://../data/dengue_clean.db", questions="dengue_clean.json", model='llama3'):
        self.questions = json.load(open(questions))
        self.bot = RegDBot(model=model)
        self.bot.set_language(config["languages"]["English"]["code"])
        self.bot.load_database(dburl)
        # self.evaluator = Factuality()

    def apply(self):
        for q in self.questions:
            question = q['question']
            context = q['context']
            expected = q['answer']
            self.bot.set_context(context)
            output = self.bot.ask(question, self.bot.active_db.tables[0])
            print(f"Question: {question}")
            print(output)
            # result = self.evaluator(output, expected, input=question)
            # print(f"Factuality score: {result.score}")
            # print(f"Factuality metadata: {result.metadata['rationale']}")



if __name__ == '__main__':
    ae = ApplyEvaluation("duckdb://../data/dengue_clean.db", "dengue_clean.json", model='gpt')
    ae.apply()
    ae2 = ApplyEvaluation(dburl="csv:../data/netflix_titles.csv", questions="netflix_titles.json", model='gpt')
    ae2.apply()


