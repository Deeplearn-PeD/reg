import pandas as pd
import pytest
import os
import duckdb
from unittest.mock import patch, Mock
from regdbot.brain import dbtools as dbt
from base_agent.llminterface import LangModel


@pytest.fixture
def memdb():
    return duckdb.connect()

tmp_path = pytest.fixture(lambda: './fixtures')


def test_get_sample_data():
    lang_model = LangModel('llama3.1')
    db = dbt.Database('csv:brain/fixtures/Star_Trek_Season_1.csv', lang_model)
    result = db._get_sample_rows('startrek_table')
    assert isinstance(result, list)
    assert len(result) == 5

def test_get_table_description():
    lang_model = LangModel('llama3.1')
    table_name = 'startrek_table'
    db = dbt.Database('csv:brain/fixtures/Star_Trek_Season_1.csv', lang_model)
    result = db.get_table_description(table_name)
    # get_table_description returns a markdown string
    assert 'season_num' in result
    assert 'episode_num' in result

def test_get_csv_description_from_url():
    file_path = 'https://blobs.duckdb.org/data/Star_Trek-Season_1.csv'
    result = dbt.get_csv_description(file_path)
    assert 'season_num' in result[0]
    assert 'episode_num' in result[1]

def test_get_csv_description_from_file():
    file_path = 'brain/fixtures/Star_Trek_Season_1.csv'
    result = dbt.get_csv_description(file_path)
    assert 'season_num' in result[0]
    assert 'episode_num' in result[1]

def test_database_connection_with_duckdb_url():
    lang_model = LangModel('llama3.1')
    db = dbt.Database('duckdb:///:memory:',lang_model)
    assert isinstance(db.connection, duckdb.DuckDBPyConnection)

def test_get_table_df_from_csv():
    lang_model = LangModel('llama3.1')
    db = dbt.Database('csv:brain/fixtures/Star_Trek_Season_1.csv', lang_model)
    result = db.get_table_df('startrek_table')
    assert result.shape == (30, 18)
    assert isinstance(result, pd.DataFrame)


def test_get_table_df_from_duckdb():
    lang_model = LangModel('llama3.1')
    db = dbt.Database('duckdb://brain/fixtures/doaj.db', lang_model)
    result = db.get_table_df('journalcsv__doaj_20240710')
    assert result.shape == (20622, 54)
    assert isinstance(result, pd.DataFrame)

def test_get_keys():
    lang_model = LangModel('llama3.1')
    db = dbt.Database('duckdb://brain/fixtures/doaj.db', lang_model)
    result, keys = db.run_query('SELECT * FROM journalcsv__doaj_20240710 LIMIT 5')
    assert keys[0] == 'Journal title'