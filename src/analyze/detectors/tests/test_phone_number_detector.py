from unittest import TestCase

from src.analyze.detectors.phone_number_detector import PhoneNumberDetector
from src.analyze.utils.analyzer_result import AnalyzerResult


class TestPhoneNumberDetector(TestCase):

    def setUp(self):
        self.phone_number_detector = PhoneNumberDetector()

    def test_default_property_values_are_correct(self):
        self.assertEqual("PHONE_NUMBER", self.phone_number_detector.name)
        self.assertEqual('(\\+65?\\s?[689]\\d{7})|'
                         '(\\+65?\\s?[689]\\d{3} \\d{4})|'
                         '([689]\\d{7})|'
                         '([689]\\d{3} \\d{4})|'
                         '([(]65[)]\\s?[689]\\d{7})|'
                         '([(]65[)]\\s?[689]\\d{3} \\d{4})',
                         self.phone_number_detector.pattern)

    def test_invalid_phone_number_does_not_get_detected(self):
        self.assertEqual(len(self.phone_number_detector.execute("S0000001I")), 0)

    def __assert_single_result(self, text_to_be_tested, start, end):
        actual = self.phone_number_detector.execute(text_to_be_tested)
        expected = AnalyzerResult(text_to_be_tested, "PHONE_NUMBER", start, end)
        self.assertEqual(len(actual), 1)
        self.assertEqual(expected, actual[0])

    def test_valid_phone_number_gets_detected_correctly(self):
        self.__assert_single_result("+65 65781234", 0, 12)
        self.__assert_single_result("+65 85781234", 0, 12)
        self.__assert_single_result("+65 95781234", 0, 12)

        self.__assert_single_result("+65 6578 1234", 0, 13)
        self.__assert_single_result("+65 8578 1234", 0, 13)
        self.__assert_single_result("+65 9578 1234", 0, 13)

        self.__assert_single_result("65781234", 0, 8)
        self.__assert_single_result("85781234", 0, 8)
        self.__assert_single_result("95781234", 0, 8)

        self.__assert_single_result("6578 1234", 0, 9)
        self.__assert_single_result("8578 1234", 0, 9)
        self.__assert_single_result("9578 1234", 0, 9)

        self.__assert_single_result("(65) 65781234", 0, 13)
        self.__assert_single_result("(65) 85781234", 0, 13)
        self.__assert_single_result("(65) 95781234", 0, 13)

        self.__assert_single_result("(65) 6578 1234", 0, 14)
        self.__assert_single_result("(65) 8578 1234", 0, 14)
        self.__assert_single_result("(65) 9578 1234", 0, 14)
