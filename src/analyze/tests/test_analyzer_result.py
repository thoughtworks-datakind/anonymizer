from analyze.analyzer_result import AnalyzerResult
from unittest import TestCase


class TestAnalyzerResult(TestCase):

    def test_equality(self):
        expected = AnalyzerResult("text", "type", 0, 10)
        actual = AnalyzerResult("text", "type", 0, 10)
        self.assertEqual(expected, actual)

    def test_inequality(self):
        self.assertNotEqual(AnalyzerResult("text", "type", 0, 10), AnalyzerResult("different_text", "type", 0, 10))
        self.assertNotEqual(AnalyzerResult("text", "type", 0, 10), AnalyzerResult("text", "different_type", 0, 10))
        self.assertNotEqual(AnalyzerResult("text", "type", 0, 10), AnalyzerResult("text", "type", 1, 10))
        self.assertNotEqual(AnalyzerResult("text", "type", 0, 10), AnalyzerResult("text", "type", 0, 11))
