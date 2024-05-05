import pytest
import os
import duckdb
from unittest.mock import patch, Mock
from regdbot.brain import dbtools as dbt


@pytest.fixture
def memdb():
    return duckdb.connect()

tmp_path = pytest.fixture(lambda: './fixtures')


def test_get_sample_data():
    db = dbt.Database('csv:brain/fixtures/Star_Trek-Season_1.csv')
    result = db._get_sample_rows('startrek_table')
    assert isinstance(result, list)
    assert len(result) == 5

def test_get_table_description():
    table_name = 'startrek_table'
    db = dbt.Database('csv:brain/fixtures/Star_Trek-Season_1.csv')
    result = db.get_table_description(table_name)

    assert 'season_num' in result[0]
    assert 'episode_num' in result[1]

def test_get_csv_description_from_url():
    file_path = 'https://blobs.duckdb.org/data/Star_Trek-Season_1.csv'
    result = dbt.get_csv_description(file_path)
    assert 'season_num' in result[0]
    assert 'episode_num' in result[1]

def test_get_csv_description_from_file():
    file_path = 'brain/fixtures/Star_Trek-Season_1.csv'
    result = dbt.get_csv_description(file_path)
    assert 'season_num' in result[0]
    assert 'episode_num' in result[1]

def test_database_connection_with_duckdb_url():
    db = dbt.Database('duckdb:///:memory:')
    assert isinstance(db.connection, duckdb.DuckDBPyConnection)




