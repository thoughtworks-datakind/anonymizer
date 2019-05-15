import pandas as pd
from unittest import TestCase

from src.analyze.detectors.report_generator import ReportGenerator
from src.analyze.utils.analyzer_result import AnalyzerResult


class TestReportGenerator(TestCase):

    def setUp(self):
        self.report_generator = ReportGenerator()

    def test_empty_result_data_frame_returns_empty_report(self):
        result_data_frame = pd.DataFrame({})
        self.assertTrue(self.report_generator.generate(result_data_frame).empty)

    def test_high_level_reporting_returns_columns_with_PII_values_when_given_a_results_data_frame(self):
        result_data_frame = pd.DataFrame({"summary" : [AnalyzerResult("S0000001I", "NRIC", 38, 47), AnalyzerResult("test@sample.com", "EMAIL", 45, 60)],
                                         "phone number": [AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47), AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)]})
        self.assertCountEqual(self.report_generator.generate(result_data_frame), ["summary", "phone number"])

    # def test_low_level_reporting_returns_data_frame_with_detector_level_details(self):
    #     result_data_frame = pd.DataFrame({"summary" : [AnalyzerResult("S0000001I", "NRIC", 38, 47), AnalyzerResult("test@sample.com", "EMAIL", 45, 60)],
    #                                       "phone number": [AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47), AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)]})
    #
    #     expected_data_frame = pd.DataFrame({"NRIC" : ["summary"],
    #                                       "PHONE_NUMBER": ["phone number"],
    #                                       "EMAIL" : ["summary"]})
    #     self.assertCountEqual(list(expected_data_frame), self.report_generator.generate(result_data_frame, high_level_report=False))