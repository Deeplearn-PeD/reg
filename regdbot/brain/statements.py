'''
This module contains the statements and prompts for the bot's persona.
'''

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
        'Verificando se a URL deste banco existe no ambiente...',
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