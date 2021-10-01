from unittest import TestCase
from unittest.mock import patch, MagicMock

import pandas as pd
from pandas._testing import assert_frame_equal
from freezegun import freeze_time
from pyspark.sql.session import SparkSession
from pyspark.sql.types import Row, StructField, StructType, ArrayType, StringType, LongType
from src_spark.report.report_generator import ReportGenerator
from src_spark.analyze.utils.analyzer_result import AnalyzerResult



class TestReportGenerator(TestCase):

    @patch("src_spark.report.report_generator.ReportGenerator.setup_logging_config")
    def setUp(self, mock_setup_logging_config):
        self.SPARK = SparkSession.builder \
                                .master("local") \
                                .appName("Test PIIDetector") \
                                .getOrCreate()


        self.array_structtype = StructType([
            StructField("end", LongType(), False),
            StructField("start", LongType(), False),
            StructField("text", StringType(), False),
            StructField("type", StringType(), False)
        ])
        self.schema = StructType([
            StructField("summary", ArrayType(self.array_structtype, True), nullable=False),
            StructField("phone number", ArrayType(self.array_structtype, True), nullable=False) 
        ])
        self.report_generator_high_level = ReportGenerator(config={"location" : "abc", "level" : "high"})
        mock_setup_logging_config.assert_called_with()
        self.report_generator_medium_level = ReportGenerator(config={"location" : "abc", "level" : "medium"})
        mock_setup_logging_config.assert_called_with()

    def test_high_level_reporting_returns_columns_with_PII_values_when_given_a_results_data_frame(self):
        test_data_frame = self.SPARK.createDataFrame(
            [
                ([AnalyzerResult("S0000001I", "NRIC", 38, 47)], [AnalyzerResult("test@sample.com", "EMAIL", 45, 60)]),
                ([AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)], [AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)])
            ],
            self.schema
        )
        expected_data_frame = pd.DataFrame({"Columns with PII values" : ["summary", "phone number"]})
        self.assertCountEqual(expected_data_frame, self.report_generator_high_level.generate_report_content(test_data_frame))



    def test_medium_level_reporting_returns_data_frame_with_detectors_and_column_details(self):
        test_data_frame = self.SPARK.createDataFrame(
            [
                ([AnalyzerResult("S0000001I", "NRIC", 38, 47)], [AnalyzerResult("test@sample.com", "EMAIL", 45, 60)]),
                ([AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)], [AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)])
            ],
            self.schema
        )

        expected_data_frame = pd.DataFrame({
            "summary": [(1, "50.0%"), 0, (1, "50.0%")],
            "phone number": [0, (1, "50.0%"), (1, "50.0%")]
        },index=["NRIC","EMAIL","PHONE_NUMBER"])

        self.assertCountEqual(list(expected_data_frame), self.report_generator_medium_level.spark_generate_medium_level_report(test_data_frame))

    def test_that_medium_level_reporting_returns_correct_data_frame(self):
        test_data_frame = self.SPARK.createDataFrame(
            [
                ([AnalyzerResult("S0000001I", "NRIC", 38, 47)], [AnalyzerResult("test@sample.com", "EMAIL", 45, 60)]),
                ([AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)], [AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)])
            ],
            self.schema
        )

        expected_data_frame = pd.DataFrame({
            "summary": [(1, "50.0%"), 0, (1, "50.0%")],
            "phone number": [0, (1, "50.0%"), (1, "50.0%")]
        },index=["NRIC","EMAIL","PHONE_NUMBER"])

        actual = self.report_generator_medium_level.spark_generate_medium_level_report(test_data_frame)
        assert_frame_equal(actual, expected_data_frame)

    @patch("logging.info")
    @patch("src.report.report_generator.ReportGenerator.generate_report_content")
    def test_generate_report_calls_content_generate_report_content_and_logs_it(self, mock_generate_content, mock_logging):
        test_data_frame = self.SPARK.createDataFrame(
            [
                ([AnalyzerResult("S0000001I", "NRIC", 38, 47)], [AnalyzerResult("test@sample.com", "EMAIL", 45, 60)]),
                ([AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)], [AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)])
            ],
            self.schema
        )
        mock_generate_content.return_value = pd.DataFrame({"Columns with PII values" : ["summary", "phone number"]})
        mock_logging.return_value = None
        expected_result = self.report_generator_high_level.generate(test_data_frame)
        self.assertCountEqual(expected_result, mock_generate_content.return_value)


    @freeze_time('2019-05-29 01:01:03')
    @patch("logging.FileHandler")
    @patch("logging.Logger.addHandler")
    @patch("genericpath.exists")
    def test_creation_of_the_report_file_if_not_present(self, mock_file_exists, mock_add_handler, mock_file_handler):
        mock_file_exists.return_value = False
        mock_file_handler.return_value = MagicMock()
        self.report_generator_high_level.setup_logging_config()
        mock_file_handler.assert_called_with(filename="abc/report_20190529.log", mode="x")
        mock_add_handler.assert_called_with(mock_file_handler.return_value)


    @freeze_time('2019-05-29 01:01:03')
    @patch("logging.FileHandler")
    @patch("logging.Logger.addHandler")
    @patch("os.path.exists")
    def test_appending_to_report_file_if_already_present(self, mock_file_exists, mock_add_handler, mock_file_handler):
        mock_file_exists.return_value = True
        mock_file_handler.return_value = MagicMock()
        self.report_generator_high_level.setup_logging_config()
        mock_file_handler.assert_called_with(filename="abc/report_20190529.log", mode="a")
        mock_add_handler.assert_called_with(mock_file_handler.return_value)
    
    def test_that_when_report_dataframe_contains_only_empty_lists_it_is_considered_empty(self):
        test_data_frame = self.SPARK.createDataFrame(
            [
                ([], []),
                ([], [])
            ],
            self.schema
        )

        actual = self.report_generator_medium_level.is_empty_report_dataframe(test_data_frame)
        expected = True

        self.assertEqual(actual, expected)

    def test_that_when_report_dataframe_contains_some_text_it_is_not_considered_empty(self):
        test_data_frame = self.SPARK.createDataFrame(
            [
                ([AnalyzerResult("S0000001I", "NRIC", 38, 47)], []),
                ([], [])
            ],
            self.schema
        )

        actual = self.report_generator_medium_level.is_empty_report_dataframe(test_data_frame)
        expected = False

        self.assertEqual(actual, expected)

    def test_that_get_detector_results_returns_list_of_detector_results(self):
        columns = ["summary", "phone_number"]
        test_row = Row(summary=[Row(end=47, start=38, text='S0000001I', type='NRIC')], phone_number=[Row(end=60, start=45, text='test@sample.com', type='EMAIL')])
        actual = self.report_generator_medium_level._get_detector_results(test_row, columns)
        expected = [(('summary', 'NRIC'), 1), (('phone_number', 'EMAIL'), 1)]
        self.assertEqual(actual, expected)

    def test_that_get_detector_results_returns_list_of_detector_results_if_column_is_empty(self):
        columns = ["summary", "phone_number"]
        test_row = Row(summary=[Row(end=47, start=38, text='S0000001I', type='NRIC')], phone_number=[])
        actual = self.report_generator_medium_level._get_detector_results(test_row, columns)
        expected = [(('summary', 'NRIC'), 1), (('phone_number', 'no_pii'), 1)]
        self.assertEqual(actual, expected)
        
