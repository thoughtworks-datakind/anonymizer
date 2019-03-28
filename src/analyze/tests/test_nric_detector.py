from unittest import TestCase
from analyze.nric_detector import NRICDetector


class TestNRICDetector(TestCase):

    def setUp(self):
        self.nric_detector = NRICDetector()

    def test_default_property_values_are_correct(self):
        self.assertEqual("NRIC", self.nric_detector.name)
        self.assertEqual("[STFG]\\d{7}[A-Z]", self.nric_detector.pattern)

    def test_additional_checks_should_return_true_when_given_valid_input(self):
        self.assertTrue(self.nric_detector.validate("S0000001I"))

    def test_additional_checks_should_return_true_when_given_invalid_input(self):
        self.assertFalse(self.nric_detector.validate("S0000001K"))
