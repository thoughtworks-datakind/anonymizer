from src.analyze.detectors.base_detector import BaseDetector
from src.analyze.utils.regex import RegEx


class CreditCardDetector(BaseDetector):

    def __init__(self):
        self.name = "CREDIT_CARD"
        self.pattern = RegEx().literal("4").any_digit().num_occurrences(3).pipe() \
            .literal("5").range(0, 5).any_digit().num_occurrences(2).pipe() \
            .literal("6").any_digit().num_occurrences(3).pipe() \
            .literal("1").any_digit().num_occurrences(3).pipe() \
            .literal("3").any_digit().num_occurrences(3) \
            .one_of("- ").zero_or_one_occurrences() \
            .any_digit().range_occurrences(3, 4) \
            .one_of("- ").zero_or_one_occurrences() \
            .any_digit().range_occurrences(3, 4) \
            .one_of("- ").zero_or_one_occurrences() \
            .any_digit().range_occurrences(3, 5).build()

    def get_name(self):
        return self.name

    def get_pattern(self):
        return self.pattern

    def validate(self, text):
        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(text.replace('-', '').replace(' ', ''))
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)

        for d in even_digits:
            checksum += sum(digits_of(d * 2))

        return checksum % 10 == 0
