from unittest import TestCase
from analyze.email_detector import EmailDetector


class TestEmailDetector(TestCase):

    def test_default_property_values_are_correct(self):
        email_detector = EmailDetector()
        self.assertEqual("EMAIL", email_detector.name)
        self.assertEqual("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+", email_detector.pattern)

