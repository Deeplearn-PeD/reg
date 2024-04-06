"""
This package defines a basic AI bot's Personality.
Starting with a Base class setting the basic parameters
for Such as name, language model uses, and basic context sqlprompts defining its purpose.
"""
from regdbot.voice import talk
from regdbot.persona_prompts import sql_retrieval_augmented
from typing import List, Dict, Any, Union



class Persona:
    def __init__(self, name: str='Reggie D. Bot', model: str='gpt-4',  languages=['pt_BR','en'], context_prompts: List[str] = None):
        self.name = name
        self.languages = languages
        self.active_language = languages[0]
        self.model = None
        self.voice = talk.Speaker(voice=talk.piper_languages[self.active_language], language=self.active_language)
        self.say = self.voice.say
        self.context_prompt = sql_retrieval_augmented + '' if context_prompts is None else '\n'.join(context_prompts)

    def set_language(self, language: str):
        if language in self.languages:
            self.active_language = language
            self.voice = talk.Speaker(voice=talk.piper_languages[self.active_language], language=self.active_language)
            self.say = self.voice.say
        else:
            raise ValueError(f"Language {language} not supported by this persona.")

