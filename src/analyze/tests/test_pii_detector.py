from unittest import TestCase
from analyze.pii_detector import PIIDetector


class TestPIIDetector(TestCase):

    def test_should_detect_nric_in_text(self):
        results = PIIDetector.analyze("Hi customer care executive my nric number is G3309008R")
        self.assertEqual("The text G3309008R at position(45,54) was identified as NRIC", results[0])
