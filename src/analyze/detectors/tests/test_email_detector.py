from unittest import TestCase
from unittest.mock import patch

from src.analyze.detectors.email_detector import EmailDetector


class TestEmailDetector(TestCase):

    def setUp(self):
        self.email_detector = EmailDetector()

    def test_get_name_returns_the_valid_detector_name(self):
        self.assertEqual(self.email_detector.get_name(), "EMAIL")

    def test_get_pattern_returns_compiled_regex(self):
        actual_value = self.email_detector.get_pattern()
        return_value = "[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+"
        self.assertEqual(return_value, actual_value)

    def test_valid_email_gets_detected_correctly(self):
        self.assertEqual(len(self.email_detector.execute("abc@hotmail.com")), 1)

    def test_invalid_email_does_not_get_detected(self):
        self.assertEqual(len(self.email_detector.execute("@hotmail.com")), 0)
