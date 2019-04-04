from unittest import TestCase

from src.analyze.detectors.credit_card_detector import CreditCardDetector


class TestCreditCardDetector(TestCase):

    def setUp(self):
        self.credit_card_detector = CreditCardDetector()

    def test_default_property_values_are_correct(self):
        self.assertEqual("CREDIT_CARD", self.credit_card_detector.name)
        self.assertEqual('4\\d{3}|5[0-5]\\d{2}|6\\d{3}|1\\d{3}|3\\d{3}[- ]?\\d{3,4}[- ]?\\d{3,4}[- ]?\\d{3,5}',
                         self.credit_card_detector.pattern)

    def test_valid_credit_cards(self):
        self.assertTrue(self.credit_card_detector.validate("4012888888881881"))
        self.assertTrue(self.credit_card_detector.validate("4012-8888-8888-1881"))
        self.assertTrue(self.credit_card_detector.validate("4012 8888 8888 1881"))

    def test_valid_airplus_credit_card(self):
        self.assertTrue(self.credit_card_detector.validate('122000000000003'))

    def test_valid_amex_credit_card(self):
        self.assertTrue(self.credit_card_detector.validate('371449635398431'))

    def test_valid_cartebleue_credit_card(self):
        self.assertTrue(self.credit_card_detector.validate('5555555555554444'))

    def test_valid_dankort_credit_card(self):
        self.assertTrue(self.credit_card_detector.validate('5019717010103742'))

    def test_valid_diners_credit_card(self):
        self.assertTrue(self.credit_card_detector.validate('30569309025904'))

    def test_valid_discover_credit_card(self):
        self.assertTrue(self.credit_card_detector.validate('6011000400000000'))

    def test_valid_jcb_credit_card(self):
        self.assertTrue(self.credit_card_detector.validate('3528000700000000'))

    def test_valid_maestro_credit_card(self):
        self.assertTrue(self.credit_card_detector.validate('6759649826438453'))

    def test_valid_mastercard_credit_card(self):
        self.assertTrue(self.credit_card_detector.validate('5555555555554444'))

    def test_valid_visa_credit_card(self):
        self.assertTrue(self.credit_card_detector.validate('4111111111111111'))

    def test_valid_visa_debit_credit_card(self):
        self.assertTrue(self.credit_card_detector.validate('4111111111111111'))

    def test_valid_visa_electron_credit_card(self):
        self.assertTrue(self.credit_card_detector.validate('4917300800000000'))

    def test_valid_visa_purchasing_credit_card(self):
        self.assertTrue(self.credit_card_detector.validate('4484070000000000'))

    def test_invalid_credit_card(self):
        self.assertFalse(self.credit_card_detector.validate('4012-8888-8888-1882'))

    def test_invalid_diners_card(self):
        self.assertFalse(self.credit_card_detector.validate('36168002586008'))
