from context import csv_parser
import unittest

class TestCsvParser(unittest.TestCase) : 

    def test_if_file_path_is_empty_throws_error(self) : 
        self.assertRaises(FileNotFoundError, lambda: csv_parser.parse("")) 

    def test_if_file_not_present_throws_error(self) : 
        self.assertRaises(FileNotFoundError, lambda: csv_parser.parse("invalid_file_path"))


if __name__ == '__main__':
    unittest.main()