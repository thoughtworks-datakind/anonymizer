from analyze.base_detector import BaseDetector
from analyze.regex import RegEx


class PhoneNumberDetector(BaseDetector):

    def __init__(self):
        self.name = "PHONE NUMBER"
        self.pattern = RegEx()\
            .one_of("+").zero_or_more_occurrences()\
            .one_of("(").zero_or_one_occurrences()\
            .range(0, 9).range_occurrences(1, 4)\
            .one_of(")").zero_or_one_occurrences()\
            .one_of("-\s\./0-9").zero_or_more_occurrences().build()
