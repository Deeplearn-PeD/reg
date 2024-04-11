import pytest
import os
import duckdb
from unittest.mock import patch, Mock
from regdbot.brain import dbtools as dbt


@pytest.fixture
def memdb():
    return duckdb.connect()

tmp_path = pytest.fixture(lambda: './fixtures')



# def test_get_table_description():
#     table_name = 'startrek_table'
#     conn = sqlgen.get_duckdb_connection('duckdb:///:memory:')
#     query1 = f"CREATE TABLE {table_name} as SELECT * FROM read_csv('fixtures/Star_Trek-Season_1.csv');"
#
#     conn.execute(query1)
#     result = dbt.get_table_description(conn, table_name)
#
#     assert 'season_num' in result[0]
#     assert 'episode_num' in result[1]

def test_get_csv_description_from_url():
    file_path = 'https://blobs.duckdb.org/data/Star_Trek-Season_1.csv'
    result = dbt.get_csv_description(file_path)
    assert 'season_num' in result[0]
    assert 'episode_num' in result[1]

def test_get_csv_description_from_file():
    file_path = 'fixtures/Star_Trek-Season_1.csv'
    result = dbt.get_csv_description(file_path)
    assert 'season_num' in result[0]
    assert 'episode_num' in result[1]

def test_database_connection_with_duckdb_url():
    with patch('regdbot.brain.dbtools.get_duckdb_connection') as mock_get_duckdb_connection:
        db = dbt.Database('duckdb:///:memory:')
        db.connection
        mock_get_duckdb_connection.assert_called_once_with('duckdb:///:memory:')

def test_database_connection_with_postgresql_url():
    with patch('sqlalchemy.create_engine') as mock_create_engine:
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        db = dbt.Database('postgresql://localhost/test')
        db.connection
        mock_create_engine.assert_called_once_with('postgresql://localhost/test')
        mock_engine.connect.assert_called_once()

def test_database_connection_with_unsupported_url():
    with patch('loguru.logger.error') as mock_error:
        db = dbt.Database('unsupported://localhost/test')
        db.connection
        mock_error.assert_called_once_with('Database URL unsupported://localhost/test not supported.')

def test_get_table_description():
    with patch.object(dbt.Database, 'connection') as mock_connection:
        mock_execute = Mock()
        mock_connection.execute.return_value = mock_execute
        db = dbt.Database('duckdb:///:memory:')
        db.get_table_description('table_name')
        mock_execute.execute.assert_called_once_with('DESCRIBE SELECT * FROM table_name;')

def test_tables_property():
    with patch.object(dbt.Database, 'connection') as mock_connection:
        mock_execute = Mock()
        mock_execute.fetchall.return_value = [('table1',), ('table2',)]
        mock_connection.execute.return_value = mock_execute
        db = dbt.Database('duckdb:///:memory:')
        assert db.tables == ['table1', 'table2']
        assert db.tables == ['table1', 'table2']
        mock_connection.execute.assert_called_once_with('SELECT table_name FROM information_schema.tables WHERE table_schema = \'main\';')
        mock_execute.fetchall.assert_called_once()