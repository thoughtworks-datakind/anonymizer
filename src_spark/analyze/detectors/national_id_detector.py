from src_spark.analyze.detectors.base_detector import BaseDetector
from src_spark.analyze.utils.regex import RegEx


class NationalIdDetector(BaseDetector):

    def __init__(self):
        self.name = "NRIC"
        self.pattern = RegEx().one_of("STFG").any_digit().num_occurrences(7).range("A", "Z").build()

    def get_name(self):
        return self.name

    def get_pattern(self):
        return self.pattern

    def __get_offset(self, text):
        return 4 if text in "TG" else 0

    def __is_NRIC(self, text, loc):
        if text[0] in "ST":
            return "JZIHGFEDCBA"[loc] == text[8]
        return False

    def __is_FIN(self, text, loc):
        if text[0] in "FG":
            return "XWUTRQPNMLK"[loc] == text[8]
        return False

    def validate(self, text):
        weight = self.__get_weight(text)
        first_character = text[0]
        offset = self.__get_offset(first_character)
        loc = (offset + weight) % 11
        return self.__is_NRIC(text, loc) or self.__is_FIN(text, loc)

    def __get_weight(self, text):
        numbers = [int(digit) for digit in list(text[1:-1])]
        for index, i in enumerate(numbers):
            if index == 0:
                numbers[index] *= 2
            numbers[index] *= 8 - index
        return sum(numbers)
