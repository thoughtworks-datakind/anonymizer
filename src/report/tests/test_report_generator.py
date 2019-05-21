from unittest import TestCase

import numpy as np
import pandas as pd

from src.report.report_generator import ReportGenerator, ReportLevel
from src.analyze.utils.analyzer_result import AnalyzerResult


class TestReportGenerator(TestCase):

    def setUp(self):
        self.report_generator = ReportGenerator()

    def test_empty_result_data_frame_returns_empty_report(self):
        result_data_frame = pd.DataFrame({})
        self.assertTrue(self.report_generator.generate(result_data_frame).empty)

    def test_high_level_reporting_returns_columns_with_PII_values_when_given_a_results_data_frame(self):
        result_data_frame = pd.DataFrame({"summary" : [[AnalyzerResult("S0000001I", "NRIC", 38, 47)], [AnalyzerResult("test@sample.com", "EMAIL", 45, 60)]],
                                         "phone number": [[AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)], [AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)]]})
        self.assertCountEqual(self.report_generator.generate(result_data_frame), ["summary", "phone number"])

    def test_medium_level_reporting_returns_data_frame_with_detectors_and_column_details(self):
        result_data_frame = pd.DataFrame({"summary" : [[AnalyzerResult("S0000001I", "NRIC", 38, 47)], [AnalyzerResult("test@sample.com", "EMAIL", 45, 60)]],
                                          "phone number": [[AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)], [AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)]]})
        expected_data_frame = pd.DataFrame({"summary" : pd.Series({"NRIC" : 1, "EMAIL" : 1}),
                                           "phone number" : pd.Series({"PHONE_NUMBER" : 2})})
        self.assertCountEqual(list(expected_data_frame), self.report_generator.generate(result_data_frame, report_level=ReportLevel.MEDIUM))

    def test_calculate_detector_counts_skims_through_a_column_and_counts_detector_results_in_each_of_them(self):
        result_column_values = pd.Series([[AnalyzerResult("S0000001I", "NRIC", 38, 47)], [AnalyzerResult("test@sample.com", "EMAIL", 45, 60)], [AnalyzerResult("test@sample.com", "EMAIL", 45, 60)]])
        actual_result = self.report_generator.calculate_detector_counts_for_each_column(result_column_values)
        expected_result = {"NRIC" : 1, "EMAIL" : 2}
        self.assertCountEqual(expected_result, actual_result)
