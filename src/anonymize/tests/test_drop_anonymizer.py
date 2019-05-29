from unittest import TestCase
from src.anonymize.drop_anonymizer import DropAnonymizer
from src.analyze.utils.analyzer_result import AnalyzerResult


class TestDropAnonymizer(TestCase):

    def test_execute_calls_match_and_validate(self):
        text = "text containing pii"
        analyzer_results = [AnalyzerResult("pii", "ANY_PII_DETECTOR", 27, 29)]
        result = DropAnonymizer.redact(text, analyzer_results)
        self.assertEqual(result, "text containing ")

