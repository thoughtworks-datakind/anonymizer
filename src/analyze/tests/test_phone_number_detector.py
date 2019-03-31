from unittest import TestCase
from src.analyze.phone_number_detector import PhoneNumberDetector


class TestPhoneNumberDetector(TestCase):

    def test_default_property_values_are_correct(self):
        phone_number_detector = PhoneNumberDetector()
        self.assertEqual("PHONE NUMBER", phone_number_detector.name)
        self.assertEqual('[+]*[(]?[0-9]{1,4}[)]?[-\\s\\./0-9]*', phone_number_detector.pattern)
