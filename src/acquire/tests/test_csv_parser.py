from unittest import TestCase
import os
import pandas as pd
from src.acquire.csv_parser import CsvParser


class TestCsvParser(TestCase):

    def setUp(self):
        self.current_dir = os.path.dirname(os.path.realpath(__file__))

    def test_invalid_config_gets_caught_during_initialization(self):
        context = {}
        with self.assertRaises(ValueError) as ve:
            CsvParser(config=context)
        self.assertEqual(str(ve.exception), "Config 'file_path' needs to be provided for parsing")

    def test_if_valid_csv_file_provided_returns_pandas_df(self):
        file_path = "{}/data/comma_delimited_file.csv".format(self.current_dir)
        config = {"file_path" : file_path, "delimiter" : ""}
        test_csv_parser_valid_file_path = CsvParser(config=config)
        expected = pd.DataFrame({"name": ["Lisa Beard"], "ssn": ["557-39-2479"]})
        actual = test_csv_parser_valid_file_path.parse()
        self.assertEqual(actual.to_dict(), expected.to_dict())

    def test_if_valid_csv_file_with_different_delimiter_provided_returns_pandas_df(self):
        file_path = "{}/data/pipe_delimited_file.csv".format(self.current_dir)
        config = {"file_path" : file_path, "delimiter" : "|"}
        test_csv_parser_valid_file_path = CsvParser(config=config)
        expected = pd.DataFrame({"name": ["Lisa Beard"], "ssn": ["557-39-2479"]})
        actual = test_csv_parser_valid_file_path.parse()
        self.assertEqual(actual.to_dict(), expected.to_dict())

    def test_if_empty_csv_file_returns_empty_pandas_df(self):
        file_path = "{}/data/empty.csv".format(self.current_dir)
        config = {"file_path" : file_path}
        test_csv_parser_valid_file_path = CsvParser(config=config)
        expected = pd.DataFrame({})
        actual = test_csv_parser_valid_file_path.parse()
        self.assertEqual(actual.to_dict(), expected.to_dict())

    def test_if_error_is_raised_if_df_has_null_values(self):
        file_path = "{}/data/missing_comma.csv".format(self.current_dir)
        config = {"file_path" : file_path}
        with self.assertRaises(ValueError) as ve:
            CsvParser(config=config).parse()
        self.assertEqual(str(ve.exception), "Dataframe contains NULL values")
