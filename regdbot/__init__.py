"""
This package defines a basic AI bot's Personality.
Starting with a Base class setting the basic parameters
for Such as name, language model uses, and basic context sqlprompts defining its purpose.
"""
import os
from base_agent.voice import talk
from regdbot.persona_prompts import sql_retrieval_augmented
from base_agent import BasePersona
import yaml


def load_config():
    current_dir = os.path.dirname(__file__)
    config_file = os.path.join(current_dir, "config.yml")
    with open(config_file, "r") as f:
        return yaml.load(f, Loader=yaml.FullLoader)


config = load_config()
languages = ["pt_BR", "en_US"]


class Persona(BasePersona):
    def __init__(self, name: str = 'Reggie D. Bot', model: str = 'gpt-4o'):
        super().__init__(name=name, model=model, languages=languages)
        self.name = name
        self.languages = languages
        self.active_language = languages[0]
        self.context_prompt = sql_retrieval_augmented[self.active_language]

    def set_language(self, language: str):
        if language in self.languages:
            self.active_language = language
            self.voice = talk.Speaker(language=self.active_language)
            self.say = self.voice.say
            self.context_prompt = sql_retrieval_augmented[self.active_language]
        else:
            raise ValueError(f"Language {language} not supported by this persona.")
