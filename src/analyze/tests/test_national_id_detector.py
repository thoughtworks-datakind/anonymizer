from unittest import TestCase
from analyze.national_id_detector import NationalIdDetector


class TestNationalIdDetector(TestCase):

    def setUp(self):
        self.national_id_detector = NationalIdDetector()

    def test_default_property_values_are_correct(self):
        self.assertEqual("NRIC", self.national_id_detector.name)
        self.assertEqual("[STFG]\\d{7}[A-Z]", self.national_id_detector.pattern)

    def test_additional_checks_should_return_true_when_given_valid_input(self):
        self.assertTrue(self.national_id_detector.validate("S0000001I"))

    def test_additional_checks_should_return_true_when_given_invalid_input(self):
        self.assertFalse(self.national_id_detector.validate("S0000001K"))
