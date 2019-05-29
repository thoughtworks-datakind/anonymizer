from unittest import TestCase
from unittest.mock import patch, MagicMock

import os
import pandas as pd
from freezegun import freeze_time

from src.report.report_generator import ReportGenerator
from src.analyze.utils.analyzer_result import AnalyzerResult




class TestReportGenerator(TestCase):

    @patch("src.report.report_generator.ReportGenerator.setup_logging_config")
    def setUp(self, mock_setup_logging_config):
        self.report_generator_high_level = ReportGenerator(config={"location" : "abc", "level" : "high"})
        mock_setup_logging_config.assert_called_with()
        self.report_generator_medium_level = ReportGenerator(config={"location" : "abc", "level" : "medium"})
        mock_setup_logging_config.assert_called_with()

    def test_high_level_reporting_returns_columns_with_PII_values_when_given_a_results_data_frame(self):
        result_data_frame = pd.DataFrame({"summary" : [[AnalyzerResult("S0000001I", "NRIC", 38, 47)], [AnalyzerResult("test@sample.com", "EMAIL", 45, 60)]],
                                         "phone number": [[AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)], [AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)]]})
        expected_data_frame = pd.DataFrame({"Columns with PII values" : ["summary", "phone number"]})
        self.assertCountEqual(expected_data_frame, self.report_generator_high_level.generate_report_content(result_data_frame))

    def test_medium_level_reporting_returns_data_frame_with_detectors_and_column_details(self):
        result_data_frame = pd.DataFrame({"summary" : [[AnalyzerResult("S0000001I", "NRIC", 38, 47)], [AnalyzerResult("test@sample.com", "EMAIL", 45, 60)]],
                                          "phone number": [[AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)], [AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)]]})
        expected_data_frame = pd.DataFrame({"summary" : pd.Series({"NRIC" : (1, "50%"), "EMAIL" : (1,"50%")}),
                                           "phone number" : pd.Series({"PHONE_NUMBER" : (2, "100%")})})
        self.assertCountEqual(list(expected_data_frame), self.report_generator_medium_level.generate_report_content(result_data_frame))

    def test_calculate_detector_stats_returns_detector_counts_and_percentages(self):
        result_column_values = pd.Series([[AnalyzerResult("S0000001I", "NRIC", 38, 47)], [AnalyzerResult("test@sample.com", "EMAIL", 45, 60)], [AnalyzerResult("test@sample.com", "EMAIL", 45, 60)]])
        actual_result = self.report_generator_medium_level.calculate_detector_stats_for_each_column(result_column_values)
        expected_result = {"NRIC" : (1, "33.33%"), "EMAIL" : (2, "66.67%")}
        self.assertCountEqual(expected_result, actual_result)

    @patch("logging.info")
    @patch("src.report.report_generator.ReportGenerator.generate_report_content")
    def test_generate_report_calls_content_generate_report_content_and_logs_it(self, mock_generate_content, mock_logging):
        result_data_frame = pd.DataFrame({"summary" : [[AnalyzerResult("S0000001I", "NRIC", 38, 47)], [AnalyzerResult("test@sample.com", "EMAIL", 45, 60)]],
                                         "phone number": [[AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)], [AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)]]})
        mock_generate_content.return_value = pd.DataFrame({"Columns with PII values" : ["summary", "phone number"]})
        mock_logging.return_value = None
        expected_result = self.report_generator_high_level.generate(result_data_frame)
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
