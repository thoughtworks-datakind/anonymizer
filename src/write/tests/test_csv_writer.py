from src.write.csv_writer import CsvWriter
from unittest import TestCase
import os
import pandas as pd


class TestCsvWriter(TestCase):

    #TODO: check acquire file path exists
    def test_invalid_config_gets_caught_during_initialization(self):
        context = {}
        with self.assertRaises(ValueError) as ve:
            CsvWriter(config=context)
        self.assertEqual(str(ve.exception), "Config 'output_file_path' needs to be provided for parsing")


    def test_correct_output_path_is_generated(self):
        context = {
            "acquire": {
                "file_path": "/anonymizer/test_data.csv",
                "delimiter": ","
            },
            "anonymize": {
                "output_file_path" : "/anonymizer/output"
            }
        }
        input_file_name = "test_data"
        output_directory = "/anonymizer/output"
        expected = f"{output_directory}/{input_file_name}_anonymized_.csv"
        writer = CsvWriter(config=context)
        self.assertEqual(writer.get_output_file_path(), expected)