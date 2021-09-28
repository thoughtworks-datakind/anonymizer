from src_spark.analyze.detectors.base_detector import BaseDetector
from src_spark.analyze.utils.regex import RegEx


class PhoneNumberDetector(BaseDetector):

    def __init__(self):
        self.name = "PHONE_NUMBER"
        regex_pipe = RegEx().pipe().build()

        regex_with_country_code_and_no_space = '(\\+65?\\s?[689]\\d{7})'
        regex_with_country_code_and_single_space = '(\\+65?\\s?[689]\\d{3} \\d{4})'
        regex_no_country_code_and_no_space = '([689]\\d{7})'
        regex_no_country_code_and_single_space = '([689]\\d{3} \\d{4})'
        regex_with_country_code_in_brackets_and_no_space = '([(]65[)]\\s?[689]\\d{7})'
        regex_with_country_code_in_brackets_and_single_space = '([(]65[)]\\s?[689]\\d{3} \\d{4})'

        self.pattern = regex_with_country_code_and_no_space + regex_pipe + \
            regex_with_country_code_and_single_space + regex_pipe + \
            regex_no_country_code_and_no_space + regex_pipe + \
            regex_no_country_code_and_single_space + regex_pipe + \
            regex_with_country_code_in_brackets_and_no_space + regex_pipe + \
            regex_with_country_code_in_brackets_and_single_space

    def get_name(self):
        return self.name

    def get_pattern(self):
        return self.pattern
