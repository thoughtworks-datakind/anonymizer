import re

from src.analyze.base_detector import BaseDetector


class PhoneNumberDetector(BaseDetector):

    def __init__(self):
        self.name = "PHONE_NUMBER"
        self.pattern = '(\\+65?\\s?[689]\\d{7})|' \
                       '(\\+65?\\s?[689]\\d{3} \\d{4})|' \
                       '([689]\\d{7})|' \
                       '([689]\\d{3} \\d{4})|' \
                       '([(]65[)]\\s?[689]\\d{7})|' \
                       '([(]65[)]\\s?[689]\\d{3} \\d{4})'

    def get_name(self):
        return self.name

    def get_pattern(self):
        return re.compile(self.pattern)
