from unittest import TestCase
from src.analyze.pii_detector import PIIDetector
from src.analyze.analyzer_result import AnalyzerResult


class TestPIIDetector(TestCase):

    #TODO add negative tests
    def test_should_detect_nric_in_text(self):
        results = PIIDetector.analyze("First President of Singapore NRIC was S0000001I")
        self.assertEqual(AnalyzerResult("S0000001I", "NRIC", 38, 47), results[0])

    def test_should_detect_email_in_text(self):
        results = PIIDetector.analyze("A typical email id would look something like test@sample.com")
        self.assertEqual(AnalyzerResult("test@sample.com", "EMAIL", 45, 60), results[0])

    def test_should_detect_phone_in_text(self):
        results = PIIDetector.analyze("Some examples of phone numbers are +65 62345678")
        self.assertEqual(AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47), results[0])

    def test_should_detect_all_pii_fields_in_text(self):
        results = PIIDetector.analyze("""First President of Singapore NRIC was S0000001I.
                                         A typical email id would look something like test@sample.com""")

        self.assertEqual(AnalyzerResult("S0000001I", "NRIC", 38, 47), results[0])
        self.assertEqual(AnalyzerResult("test@sample.com", "EMAIL", 135, 150), results[1])

    def test_analyze_returns_none_when_no_PII_fields(self):
        results = PIIDetector.analyze("""First President of Singapore NRIC was ABC.
                                         A typical email id would look something like test""")
        self.assertEqual(len(results), 0)
