import unittest

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

    def test_ingestor_initializes_without_ingesting(self):
        # Given/When
        ingestor = CSVIngestor(self.test_file_path)

        # Then
        self.assertIsNone(ingestor.data)

    def test_raises_exception_when_csv_file_not_found(self):
        # Given
        ingestor = CSVIngestor('nonexistent.csv')

        # When/Then
        with self.assertRaises(FileNotFoundError):
            ingestor.ingest()
