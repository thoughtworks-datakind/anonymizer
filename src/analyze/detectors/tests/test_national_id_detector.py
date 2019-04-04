from unittest import TestCase

from src.analyze.detectors.national_id_detector import NationalIdDetector


class TestNationalIdDetector(TestCase):

    def setUp(self):
        self.national_id_detector = NationalIdDetector()

    def test_default_property_values_are_correct(self):
        self.assertEqual("NRIC", self.national_id_detector.name)
        self.assertEqual("[STFG]\\d{7}[A-Z]", self.national_id_detector.pattern)

    def test_execute_return_true_when_valid_old_NRIC(self):
        self.assertTrue(self.national_id_detector.validate("S0000001I"))

    def test_execute_return_true_when_valid_old_FIN(self):
        self.assertTrue(self.national_id_detector.validate("F0000001U"))

    def test_execute_return_true_when_valid_new_NRIC(self):
        self.assertTrue(self.national_id_detector.validate("T0000001E"))

    def test_execute_return_true_when_valid_new_FIN(self):
        self.assertTrue(self.national_id_detector.validate("G0000001P"))

    def test_execute_return_false_when_invalid_old_NRIC(self):
        self.assertFalse(self.national_id_detector.validate("S0000001K"))

    def test_execute_return_false_when_invalid_new_NRIC(self):
        self.assertFalse(self.national_id_detector.validate("F0000001V"))

    def test_execute_return_false_when_invalid_old_FIN(self):
        self.assertFalse(self.national_id_detector.validate("T0000001F"))

    def test_execute_return_false_when_invalid_new_FIN(self):
        self.assertFalse(self.national_id_detector.validate("G0000001Q"))
