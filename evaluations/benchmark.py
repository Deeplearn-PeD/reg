import json
import os
from typing import Dict, List
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
        self.results: List[Dict] = []
        self.correct_count = 0
        self.total_count = 0

    def compare_answers(self, expected: str, actual: str) -> bool:
        """Compare expected and actual answers, ignoring case and whitespace"""
        expected = expected.lower().strip()
        actual = actual.lower().strip()
        return expected == actual

    def apply(self):
        self.results = []
        self.correct_count = 0
        self.total_count = 0
        
        for q in self.questions:
            question = q['question']
            context = q['context']
            expected = q['answer']
            
            self.bot.set_context(context)
            output = self.bot.ask(question, self.bot.active_db.tables[0])
            is_correct = self.compare_answers(expected, output)
            
            if is_correct:
                self.correct_count += 1
            self.total_count += 1
            
            result = {
                'question': question,
                'expected': expected,
                'actual': output,
                'correct': is_correct
            }
            self.results.append(result)
            
            # Print formatted output
            print("\n" + "="*80)
            print(f"Question: {question}")
            print(f"Expected: {expected}")
            print(f"Actual:   {output}")
            print(f"Correct:  {'✓' if is_correct else '✗'}")
        
        # Print summary
        accuracy = (self.correct_count / self.total_count) * 100 if self.total_count > 0 else 0
        print("\n" + "="*80)
        print(f"Final Results:")
        print(f"Total Questions: {self.total_count}")
        print(f"Correct Answers: {self.correct_count}")
        print(f"Accuracy: {accuracy:.1f}%")
        print("="*80 + "\n")


if __name__ == '__main__':
    ae = ApplyEvaluation("duckdb://../data/dengue_clean.db", "dengue_clean.json", model='gpt')
    ae.apply()
    ae2 = ApplyEvaluation(dburl="csv:../data/netflix_titles.csv", questions="netflix_titles.json", model='gpt')
    ae2.apply()


