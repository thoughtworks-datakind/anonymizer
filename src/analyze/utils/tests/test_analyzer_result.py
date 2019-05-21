from unittest import TestCase

from src.analyze.utils.analyzer_result import AnalyzerResult


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

    def test_repr(self):
        expected = "Text sample_data at position (0,10) was identified as type"
        self.assertEqual(AnalyzerResult("sample_data", "type", 0, 10).__repr__(), expected)

    def test_str(self):
        expected = "Text sample_data at position (0,10) was identified as type"
        self.assertEqual(str(AnalyzerResult("sample_data", "type", 0, 10)), expected)

    def test_get_detector_fetches_detector_type_correctly(self):
        result = AnalyzerResult("text", "EMAIL", 0, 10)
        self.assertEqual(result.detector(), "EMAIL")