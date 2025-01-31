import json
import os
from typing import Dict, List
from regdbot.brain import RegDBot
from regdbot import config
import dotenv
import re

dotenv.load_dotenv()


class ApplyEvaluation:
    def __init__(self, dburl="duckdb://../data/dengue_clean.db", questions="dengue_clean.json", model='deepseek-chat'):
        self.questions = json.load(open(questions))
        self.bot = RegDBot(model=model)
        self.bot.set_language(config["languages"]["English"]["code"])
        self.bot.load_database(dburl)
        self.results: List[Dict] = []
        self.correct_count = 0
        self.total_count = 0


    def apply(self):
        self.results = []
        self.correct_count = 0
        self.total_count = 0
        
        for q in self.questions:
            question = q['question']
            context = q['context']
            expected = q['answer']
            
            self.bot.set_context(context)
            output, df = self.bot.ask(question, self.bot.active_db.tables[0])

            
            result = {
                'question': question,
                'expected': expected,
                'actual': output,
            }
            self.results.append(result)
            
            # Print formatted output
            print("\n" + "="*80)
            print(f"Question: {question}")
            print(f"Expected: {expected}")
            print(f"Actual:   {output}")
        



if __name__ == '__main__':
    ae = ApplyEvaluation("duckdb://../data/dengue_clean.db", "dengue_clean.json", model='gpt')
    ae.apply()
    ae2 = ApplyEvaluation(dburl="csv:../data/netflix_titles.csv", questions="netflix_titles.json", model='gpt')
    ae2.apply()


