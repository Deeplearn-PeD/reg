'''
This module is used to talk to the user. It uses the `piper` text to speech command to do so.
The class Speaker is used to configure the vois and language of the speaker.
The method `say` is used to speak the text.
'''
import subprocess as sp
import shlex
import loguru

logger = loguru.logger

piper_languages = {
    'pt_BR': 'faber-medium',
    'en_US': 'lessac-medium'
}

introductions = {
    'pt_BR': [
        'Olá, eu sou Réggie, seu assistente de banco de dados.',
        'Posso ajudá-lo com consultas SQL, análise e visualização de dados.',

    ],
    'en_US': [
        "Hello, I'm Reggie D. Bot, your database assistant.",
        "I can help you with SQL queries, data analysis, and data visualization.",
    ]
}

db_questions = {
    'pt_BR': [
        'Qual tipo de banco de dados você deseja consultar?',
        'Vrificando se a URL deste banco existe no ambiente...',
    ],
    'en_US': [
        'What kind of database do you wish to query?',
        'Checking if this database URL exists in the environment...',
    ]
}
table_questions = {
    'pt_BR': [
        'Qual tabela você deseja consultar?',
        'entre um ou mais nomes de tabelas:',
    ],
    'en_US': [
        'What table do you wish to query?',
        'Enter one or more table names:',
    ]
}

class Speaker:
    def __init__(self, language='pt_BR'):
        try:
            self.voice = piper_languages[language]
        except KeyError:
            logger.warning(f'Language {language} not supported, using en_US instead')
            self.voice = piper_languages['en_US']
        self.language = language
        self.model = language + '-' + self.voice
        self.outfile = '/tmp/speech.wav'

    def say(self, text):
        args = shlex.split(f'piper --model {self.model} --output-file {self.outfile} ')
        sp.Popen(args, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE).communicate(input=text.encode())
        sp.call(shlex.split(f'play {self.outfile}'))