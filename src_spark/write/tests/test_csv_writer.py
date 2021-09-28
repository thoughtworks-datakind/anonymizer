from unittest import TestCase
from pyspark.sql import SparkSession
from src_spark.write.csv_writer import CsvWriter


class TestCsvWriter(TestCase):
    
    def setUp(self) -> None:
        self.SPARK = SparkSession.builder \
                                .master("local") \
                                .appName("Test CsvWriter") \
                                .getOrCreate()

    def test_invalid_config_gets_caught_during_initialization(self):
        context = {}
        with self.assertRaises(ValueError) as ve:
            CsvWriter(self.SPARK, config=context)
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
        writer = CsvWriter(spark=self.SPARK, config=context)
        self.assertEqual(writer.get_output_file_path(), expected)

