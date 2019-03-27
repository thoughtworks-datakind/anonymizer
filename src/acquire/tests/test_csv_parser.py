from unittest import TestCase
import os
import pandas as pd

from acquire.csv_parser import CsvParser


class TestCsvParser(TestCase):

    def setUp(self):
        self.current_dir = os.path.dirname(os.path.realpath(__file__))

    def test_if_file_path_is_empty_throws_error(self):
        test_csv_parser_empty_file_path = CsvParser(input_path="")
        self.assertRaises(FileNotFoundError, lambda: test_csv_parser_empty_file_path.parse())

    def test_if_invalid_file_path_provided_throws_error(self):
        test_csv_parser_invalid_file_path = CsvParser(input_path="invalid_file_path")
        self.assertRaises(FileNotFoundError, lambda: test_csv_parser_invalid_file_path.parse())

    def test_if_valid_csv_file_provided_returns_pandas_df(self):
        test_csv_parser_valid_file_path = CsvParser(input_path="{}/data/comma_delimited_file.csv".format(self.current_dir))
        expected = pd.DataFrame({"name": ["Lisa Beard"], "ssn": ["557-39-2479"]})
        actual = test_csv_parser_valid_file_path.parse()
        self.assertEqual(actual.to_dict(), expected.to_dict())

    def test_if_valid_csv_file_with_different_delimiter_provided_returns_pandas_df(self):
        test_csv_parser_valid_file_path = CsvParser(input_path="{}/data/pipe_delimited_file.csv".format(self.current_dir), delimiter="|")
        expected = pd.DataFrame({"name": ["Lisa Beard"], "ssn": ["557-39-2479"]})
        actual = test_csv_parser_valid_file_path.parse()
        self.assertEqual(actual.to_dict(), expected.to_dict())

