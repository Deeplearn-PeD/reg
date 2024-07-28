import unittest
import os
import pandas as pd
from deltalake import DeltaTable
from pandas.testing import assert_frame_equal

from regdbot.brain.ingest import CSVIngestor


class CSVIngestorTests(unittest.TestCase):
    test_file_path = 'brain/fixtures/journalcsv__doaj_20240710.csv.gz'
    test_output_path = '/tmp/doaj'

    def setUp(self):
        self.ingestor = CSVIngestor(self.test_file_path)

    def test_csv_file_is_correctly_ingested(self):
        # Given
        expected_df = pd.read_csv('brain/fixtures/journalcsv__doaj_20240710.csv.gz')

        # When
        result_df = self.ingestor.ingest()

        # Then
        assert_frame_equal(result_df, expected_df)

    def test_data_is_written_to_delta_table(self):
        # When
        self.ingestor.ingest()
        dl = self.ingestor.to_delta(self.test_output_path)

        # Then

        self.assertIsInstance(dl, DeltaTable)


    def test_raises_exception_when_csv_file_not_found(self):
        # Given
        with self.assertRaises(FileNotFoundError):
            ingestor = CSVIngestor('nonexistent.csv')





    def test_ingest_and_write_to_database(self):
        # When
        dl = self.ingestor.to_delta(self.test_output_path)
        if os.path.exists(self.test_output_path+'.db'):
            os.remove(self.test_output_path+'.db')
        self.ingestor.to_database(f'duckdb://{self.test_output_path}.db')

        # Then
        self.assertIsInstance(dl, DeltaTable)
        self.assertTrue(len(dl.history()) > 0)
        self.assertTrue(os.path.exists('/tmp/doaj.db'))
