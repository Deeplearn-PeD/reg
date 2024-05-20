import json
import os
# from braintrust import Eval
# from autoevals import Factuality
from regdbot.brain import RegDBot
from regdbot import config
import dotenv

dotenv.load_dotenv()

questions = json.load(open('dengue_clean.json'))

Reggie = RegDBot(model='llama3')
Reggie.set_language(config["languages"]["English"]["code"])
Reggie.load_database('duckdb://../data/dengue_clean.db', dialect='duckdb')
# evaluator = Factuality()

for q in questions:
    question = q['question']
    context = q['context']
    expected = q['answer']
    Reggie.set_context(context)
    output = Reggie.ask(question)
    print(f"Question: {question}")
    print(output)
    # result = evaluator(output, expected, input=question)
    # print(f"Factuality score: {result.score}")
    # print(f"Factuality metadata: {result.metadata['rationale']}")


