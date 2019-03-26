from context import csv_parser
import unittest
import pandas as pd

class TestCsvParser(unittest.TestCase) : 

    def test_if_file_path_is_empty_throws_error(self) : 
        self.assertRaises(FileNotFoundError, lambda: csv_parser.parse("")) 

    def test_if_file_not_present_throws_error(self) : 
        self.assertRaises(FileNotFoundError, lambda: csv_parser.parse("invalid_file_path"))

    def test_if_csv_retruns_df(self) : 
        expected = pd.DataFrame({"name": ["Lisa Beard"], "ssn": ["557-39-2479"]})
        actual = csv_parser.parse("./acquire/data/comma_delimited_file.csv")
        self.assertTrue(expected.equals(actual))

if __name__ == "__main__":
    unittest.main()