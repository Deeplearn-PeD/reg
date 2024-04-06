"""
This package defines a basic AI bot's Personality.
Starting with a Base class setting the basic parameters
for Such as name, language model uses, and basic context prompts defining its purpose.
"""
from voice.talk import Speaker
from typing import List, Dict, Any, Union

base_prompt = """
You are Reggie D. Bot, a friendly AI assistant that helps users with data querying and analysis needs.
"""

class Persona:
    def __init__(self, name: str='Reggie D. Bot', languages=['pt_BR','en'], context_prompts: List[str] = None):
        self.name = name
        self.languages = languages
        self.active_language = languages[0]
        self.model = None
        self.voice = Speaker(voice='faber-medium', language=self.active_language)
        self.say = self.voice.say
        self.context_prompt = base_prompt + '' if context_prompts is None else '\n'.join(context_prompts)

    def set_language(self, language: str):
        if language in self.languages:
            self.active_language = language
            self.voice = Speaker(voice='faber-medium', language=self.active_language)
            self.say = self.voice.say
        else:
            raise ValueError(f"Language {language} not supported by this persona.")

