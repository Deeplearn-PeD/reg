"""
in This package we define the Bot's Brain, i.e. its professional profile.
What it knows, how it learns,
how it should interact with the user, and how it should respond to the user's requests.
"""
from regdbot import Persona
from openai import OpenAI
from regdbot.brain.sqlprompts import PromptTemplate
import dotenv
import os

dotenv.load_dotenv()


class RegDBot(Persona):
    def __init__(self, name: str = 'Reggie D. Bot', languages=['pt_BR', 'en'], model: str='gpt-4', context_prompts: list = None):
        super().__init__(name=name, languages=languages,model=model, context_prompts=context_prompts)
        self.openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.prompt_template = None


    def set_prompt(self, prompt_template):
        self.prompt_template = prompt_template

    def ask(self, question: str):
        response = self.get_response()

    def get_response(self, question):
        return self.openai.chat.completions.creat(
            model=self.model,
            messages=[
                {
                    'role': 'system',
                    'content': self.context_prompt
                },
                {
                    'role': 'user',
                    'content': self.prompt_template.get_prompt(question)
                }
            ]
        )

    def get_prompt(self):
        return self.context_prompt



if __name__ == '__main__':
    bot = RegDBot()
    bot.say("Hello, I'm Reggie D. Bot, your database assistant.")
    bot.say("I can help you with SQL queries, data analysis, and data visualization.")
    bot.say("What can I do for you today?")

    bot.set_template(PromptTemplate())

    while True:
        user_input = input("You: ")
        if user_input == 'exit':
            break
        bot.ask(user_input)
        response = bot.get_response()
        bot.say(response)
        print(response)