from unittest import TestCase
from src.anonymize.drop_anonymizer import DropAnonymizer
from src.analyze.utils.analyzer_result import AnalyzerResult


class TestDropAnonymizer(TestCase):

    def test_redact_for_single_analyzer_result(self):
        text = "text containing pii"
        analyzer_results = [AnalyzerResult("pii", "PII_DETECTOR", 16, 18)]
        result = DropAnonymizer.redact(text, analyzer_results)
        self.assertEqual(result, "text containing ")

    def test_redact_for_multiple_analyzer_results(self):
        text = "text containing pii1 and pii2"
        analyzer_results = [AnalyzerResult("pii1", "PII_DETECTOR", 16, 19),
                            AnalyzerResult("pii2", "PII_DETECTOR", 25, 28)]
        result = DropAnonymizer.redact(text, analyzer_results)
        self.assertEqual(result, "text containing  and ")

