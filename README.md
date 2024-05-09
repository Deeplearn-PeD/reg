# Reggie D. Bot
Reggie D. Bot is an AI specialized in Database exploration using RAG and other techniques.

![Reggie D. Bot](/reggie.jpeg)

## Setup
1. Clone the repository
2. acitvate the virtual environment with `poetry install` and then `poetry shell`
3. make sure you have sox installed on your system for the speech  interface.
4. install [ollama](https://github.com/ollama/ollama)
5. Create a `.env` file with the following variables
   1. OPENAI_API_KEY
   2. PGURL: postgresql://username:password@localhost:5432/dbnameMake sure you have a database as specified in the `PGURL` variable or a 
   7. DUCKURL: duckdb database specified in the `DUCKDB`  variable. For example: `DUCKURL=duckdb:///dengue_clean.db`
7. Run the bot in project directory with the command `reggie auto postgresql` or `reggie auto duckdb`