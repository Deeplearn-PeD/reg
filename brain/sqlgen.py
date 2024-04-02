from typing import List, Dict, Any
import dotenv
import os
import loguru
from sqlalchemy import create_engine

dotenv.load_dotenv()
logger = loguru.logger


def get_db_url(conn: str = 'PGURL') -> str:
    """
    Returns the database connection url
    as defined in the environment variable `conn` 
    :param conn: 
    :return: URL to database connection
    """
    return os.getenv("DB_URL")


def get_db() -> object:
    engine = create_engine(get_db_url())
    return engine
