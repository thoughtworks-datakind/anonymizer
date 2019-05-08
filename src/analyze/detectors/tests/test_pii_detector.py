import pandas as pd
from unittest import TestCase

from src.analyze.detectors.pii_detector import PIIDetector
from src.analyze.utils.analyzer_result import AnalyzerResult


class TestPIIDetector(TestCase):

    def setUp(self):
        self.pii_detector = PIIDetector()

    def test_should_detect_nric_in_text(self):
        results = self.pii_detector.analyze("First President of Singapore NRIC was S0000001I")
        self.assertEqual(AnalyzerResult("S0000001I", "NRIC", 38, 47), results[0])

    def test_should_detect_email_in_text(self):
        results = self.pii_detector.analyze("A typical email id would look something like test@sample.com")
        self.assertEqual(AnalyzerResult("test@sample.com", "EMAIL", 45, 60), results[0])

    def test_should_detect_phone_in_text(self):
        results = self.pii_detector.analyze("Some examples of phone numbers are +65 62345678")
        self.assertEqual(AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47), results[0])

    def test_should_detect_all_pii_fields_in_text(self):
        results = self.pii_detector.analyze("""First President of Singapore NRIC was S0000001I.
                                         A typical email id would look something like test@sample.com""")

        self.assertCountEqual([AnalyzerResult("S0000001I", "NRIC", 38, 47),
                               AnalyzerResult("test@sample.com", "EMAIL", 135, 150)], results)

    def test_analyze_returns_none_when_no_PII_fields(self):
        results = self.pii_detector.analyze("""First President of Singapore NRIC was ABC.
                                         A typical email id would look something like test""")
        self.assertEqual(len(results), 0)

    def test_analyze_data_frame_runs_analyze_against_each_cell(self):
        test_data_frame = pd.DataFrame({"summary" : ["First President of Singapore NRIC was S0000001I", "A typical email id would look something like test@sample.com"],
                                       "phone number" : ["Some examples of phone numbers are +65 62345678", "Some examples of phone numbers are +65 62345678"]})
        result_data_frame = self.pii_detector.analyze_data_frame(test_data_frame)
        expected_data_frame = pd.DataFrame({"summary" : [AnalyzerResult("S0000001I", "NRIC", 38, 47), AnalyzerResult("test@sample.com", "EMAIL", 45, 60)],
                                            "phone number": [AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47), AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)]})
        self.assertCountEqual(list(expected_data_frame), list(result_data_frame))
        print(str(result_data_frame))
