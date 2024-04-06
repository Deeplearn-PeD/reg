"""
in This package we define the Bot's Brain, i.e. its professional profile.
What it knows, how it learns,
how it should interact with the user, and how it should respond to the user's requests.
"""
from regdbot import Persona
from openai import OpenAI
from ollama import Client
from regdbot.brain.sqlprompts import PromptTemplate
import dotenv
import os

dotenv.load_dotenv()


class LLLModel:
    def __init__(self, model: str = 'gpt-4-0125-preview'):
        self.llm = OpenAI(api_key=os.getenv('OPENAI_API_KEY')) if 'gpt' in model else Client(host='http://localhost:11434')
        self.model = model

    def get_response(self, question: str, context: str = None) -> str:
        if 'gpt' in self.model:
            return self.get_gpt_response(question, context)
        elif 'gemma' in self.model:
            return self.get_gemma_response(question, context)

    def get_gpt_response(self, question: str, context: str)->str:
        response = self.llm.chat.completions.create(
            model=self.model,
            messages=[
                {
                    'role': 'system',
                    'content': context
                },
                {
                    'role': 'user',
                    'content': question
                }
            ],
            max_tokens=100,
            temperature=0.5,
            top_p=1
        )
        return response.choices[0].message.content

    def get_gemma_response(self, question: str, context: str) -> str:
        response = self.llm.generate(
            model=self.model,
            system=context,
            prompt=question,
            # messages=[
            #     {'role': 'system', 'content': context},
            #     {'role': 'user', 'content': question}
            # ],
            stream=True
        )

        return '/n'.join([resp['response'] for resp in response ])



class RegDBot(Persona):
    def __init__(self, name: str = 'Reggie D. Bot', languages=['pt_BR', 'en'], model: str='gpt-4-0125-preview', context_prompts: list = None):
        super().__init__(name=name, languages=languages,model=model, context_prompts=context_prompts)
        self.llm = LLLModel(model=model)
        self.prompt_template = None


    def set_prompt(self, prompt_template):
        self.prompt_template = prompt_template

    def ask(self, question: str):
        response = self.get_response(question)
        return response

    def get_response(self, question):
        response =  self.llm.get_response(question, self.prompt_template.system_preamble)
        return response

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