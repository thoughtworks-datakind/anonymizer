import os
from unittest import TestCase
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
from src_spark.acquire.csv_parser import CsvParser


class TestCsvParser(TestCase):

    def setUp(self) -> None:
        self.SPARK = SparkSession.builder \
                                .master("local") \
                                .appName("Test CSVParser") \
                                .getOrCreate()
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
    
    def test_invalid_config_gets_caught_during_initialization(self):
        context = {}
        with self.assertRaises(ValueError) as ve:
            CsvParser(self.SPARK, config=context)
        self.assertEqual(str(ve.exception), "Config 'file_path' needs to be provided for parsing")

    def test_if_valid_csv_file_provided_returns_spark_df(self):
        file_path = "{}/data/comma_delimited_file.csv".format(self.current_dir)
        config = {"file_path" : file_path, "delimiter" : ""}
        
        expected = self.SPARK.createDataFrame(
            [("Lisa Beard", "557-39-2479")],
            ["name", "ssn"]
        )
        actual = CsvParser(spark=self.SPARK, config=config).parse()
        
        self.assertEqual(actual.schema, expected.schema)
        self.assertEqual(actual.collect(), expected.collect())

    def test_if_valid_csv_file_with_different_delimiter_provided_returns_spark_df(self):
        file_path = "{}/data/pipe_delimited_file.csv".format(self.current_dir)
        config = {"file_path" : file_path, "delimiter" : "|"}
        
        expected = self.SPARK.createDataFrame(
            [("Lisa Beard", "557-39-2479")],
            ["name", "ssn"]
        )
        actual = CsvParser(spark=self.SPARK, config=config).parse()
        
        self.assertEqual(actual.schema, expected.schema)
        self.assertEqual(actual.collect(), expected.collect())

    def test_if_empty_csv_file_returns_empty_pandas_df(self):
        file_path = "{}/data/empty.csv".format(self.current_dir)
        config = {"file_path" : file_path}
        expected = self.SPARK.createDataFrame([], StructType([]))
        actual = CsvParser(spark=self.SPARK, config=config).parse()
        self.assertEqual(actual.schema, expected.schema)
        self.assertEqual(actual.collect(), expected.collect())
        
    