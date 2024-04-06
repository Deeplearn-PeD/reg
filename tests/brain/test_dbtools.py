import pytest
import os
import duckdb


@pytest.fixture
def memdb():
    return duckdb.connect()

tmp_path = pytest.fixture(lambda: './fixtures')

def test_get_db_url():
    os.environ['DBURL'] = 'duckdb:///:memory:'
    assert sqlgen.get_db_url('DBURL') == 'duckdb:///:memory:'

def test_get_db():
    engine = sqlgen.get_db('PGURL')
    assert isinstance(engine, object)

def test_get_table_description():
    table_name = 'startrek_table'
    conn = sqlgen.get_duckdb_connection('duckdb:///:memory:')
    query1 = f"CREATE TABLE {table_name} as SELECT * FROM read_csv('fixtures/Star_Trek-Season_1.csv');"

    conn.execute(query1)
    result = sqlgen.get_table_description(conn, table_name)

    assert 'season_num' in result[0]
    assert 'episode_num' in result[1]

def test_get_csv_description_from_url():
    file_path = 'https://blobs.duckdb.org/data/Star_Trek-Season_1.csv'
    result = sqlgen.get_csv_description(file_path)
    assert 'season_num' in result[0]
    assert 'episode_num' in result[1]

def test_get_csv_description_from_file():
    file_path = 'fixtures/Star_Trek-Season_1.csv'
    result = sqlgen.get_csv_description(file_path)
    assert 'season_num' in result[0]
    assert 'episode_num' in result[1]