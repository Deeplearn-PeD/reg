"""
in This package we define the Bot's Brain, i.e. its professional profile.
What it knows, how it learns,
how it should interact with the user, and how it should respond to the user's requests.
"""
from regdbot import Persona
from openai import OpenAI
from ollama import Client
import ollama
from base_agent.llminterface import LangModel
from regdbot.brain.sqlprompts import PromptTemplate
import dotenv
import os

dotenv.load_dotenv()



class RegDBot(Persona):
    def __init__(self, name: str = 'Reggie D. Bot', languages=['pt_BR', 'en'], model: str='gpt-4-0125-preview'):
        super().__init__(name=name, languages=languages,model=model)
        self.llm = LangModel(model=model)
        self.prompt_template = None
        self.context_prompt: str = ""

    @property
    def context(self):
        return self.context_prompt

    def set_context(self, context: str) -> None:
        self.context_prompt = context


    def set_prompt(self, prompt_template):
        self.prompt_template = prompt_template

    def ask(self, question: str):
        response = self.get_response(question)
        return response

    def get_response(self, question):
        response =  self.llm.get_response(question=question, context=self.prompt_template.get_prompt())
        return response

    def get_prompt(self):
        return self.context_prompt



