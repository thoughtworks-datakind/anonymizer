import pandas as pd
from unittest import TestCase

from src.analyze.detectors.pii_detector import PIIDetector
from src.analyze.utils.analyzer_result import AnalyzerResult
from src.anonymize.anonymizer_result import AnonymizerResult


class TestPIIDetector(TestCase):

    def setUp(self):
        self.pii_detector = PIIDetector()

    def test_should_detect_and_redact_nric_in_text(self):
        actual = self.pii_detector.analyze_and_redact("First President of Singapore NRIC was S0000001I")
        expected = AnonymizerResult("First President of Singapore NRIC was ", [AnalyzerResult("S0000001I", "NRIC", 38, 47)])
        self.assertEqual(actual, expected)

    def test_should_detect_and_redact_email_in_text(self):
        actual = self.pii_detector.analyze_and_redact("A typical email id would look something like test@sample.com")
        expected = AnonymizerResult("A typical email id would look something like ",
                                    [AnalyzerResult("test@sample.com", "EMAIL", 45, 60)])
        self.assertEqual(actual, expected)

    def test_should_detect_and_redact_phone_in_text(self):
        actual = self.pii_detector.analyze_and_redact("Some examples of phone numbers are +65 62345678")
        expected = AnonymizerResult("Some examples of phone numbers are ",
                                    [AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)])
        self.assertEqual(actual, expected)

    def test_should_detect_and_redact_all_pii_fields_in_text(self):
        actual = self.pii_detector.analyze_and_redact("""First President of Singapore NRIC was S0000001I.
                                         A typical email id would look something like test@sample.com""")
        expected_redacted_text = """First President of Singapore NRIC was .
                                         A typical email id would look something like """

        expected = AnonymizerResult(expected_redacted_text, [AnalyzerResult("test@sample.com", "EMAIL", 135, 150),
                                                             AnalyzerResult("S0000001I", "NRIC", 38, 47)])
        self.assertEqual(actual, expected)

    def test_analyze_returns_returns_same_text_and_no_results_when_no_PII_fields(self):
        input_text = """First President of Singapore NRIC was ABC.
                                         A typical email id would look something like test"""
        actual = self.pii_detector.analyze_and_redact(input_text)
        expected = AnonymizerResult(input_text, [])
        self.assertEqual(actual, expected)

    def test_analyze_data_frame_runs_analyze_against_each_cell_with_a_PII_value(self):
        test_data_frame = pd.DataFrame({"summary": ["First President of Singapore NRIC was S0000001I",
                                                    "A typical email id would look something like test@sample.com"],
                                        "phone number": ["Some examples of phone numbers are +65 62345678",
                                                         "Some examples of phone numbers are +65 62345678"]})

        actual, _ = self.pii_detector.analyze_data_frame(test_data_frame)

        expected_data_frame = pd.DataFrame({"summary": [[AnalyzerResult("S0000001I", "NRIC", 38, 47)],
                                                        [AnalyzerResult("test@sample.com", "EMAIL", 45, 60)]],
                                            "phone number": [[AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)],
                                                             [AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)]]})

        pd.testing.assert_frame_equal(expected_data_frame, actual)

    def test_analyze_data_frame_runs_analyze_against_each_cell_when_there_are_no_PII_values_returns_empty_data_frame(
            self):
        test_data_frame = pd.DataFrame({"summary": ["First President of Singapore NRIC was abcde",
                                                    "A typical email id would look something like test@t"],
                                        "phone number": ["Some examples of phone numbers are +34342",
                                                         "Some examples of phone numbers are +8909"]})
        expected_report = pd.DataFrame({"summary": [[],[]],
                                        "phone number": [[],[]]
                                        })
        expected_result = pd.DataFrame({"summary": ["First President of Singapore NRIC was abcde",
                                                    "A typical email id would look something like test@t"],
                                        "phone number": ["Some examples of phone numbers are +34342",
                                                         "Some examples of phone numbers are +8909"]})
        actual_report, actual_result = self.pii_detector.analyze_data_frame(test_data_frame)
        
        pd.testing.assert_frame_equal(expected_report, actual_report)
        pd.testing.assert_frame_equal(expected_result, actual_result)

    def test_analyze_data_frame_runs_analyze_only_on_cells_with_a_PII_value(self):
        test_data_frame = pd.DataFrame({"summary": ["First President of Singapore NRIC was S0000001I",
                                                    "A typical email id would look something like test@sample.com"],
                                        "remarks": ["No sensitive data",
                                                         "No sensitive data"]})

        actual_report, actual_result = self.pii_detector.analyze_data_frame(test_data_frame)

        expected_report = pd.DataFrame({"summary": [[AnalyzerResult("S0000001I", "NRIC", 38, 47)],
                                                        [AnalyzerResult("test@sample.com", "EMAIL", 45, 60)]],
                                        "remarks": [[],[]]
                                        })
                                            
        expected_result = pd.DataFrame({"summary": ["First President of Singapore NRIC was ",
                                                    "A typical email id would look something like "],
                                        "remarks": ["No sensitive data",
                                                         "No sensitive data"]})

        pd.testing.assert_frame_equal(expected_report, actual_report)
        pd.testing.assert_frame_equal(expected_result, actual_result)