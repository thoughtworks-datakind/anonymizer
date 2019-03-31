from src.analyze.base_detector import BaseDetector
from src.analyze.regex import RegEx


class NationalIdDetector(BaseDetector):

    def __init__(self):
        self.name = "NRIC"
        self.pattern = RegEx().one_of("STFG").any_digit().num_occurrences(7).range("A", "Z").build()

    def validate(self, text):
        first_character = text[0]

        weight = self.__get_weight(text)
        offset = 4 if first_character in "TG" else 0
        loc = (offset + weight) % 11

        if first_character in "ST":
            return "JZIHGFEDCBA"[loc] == text[8]
        if first_character in "FG":
            return "XWUTRQPNMLK"[loc] == text[8]

    @staticmethod
    def __get_weight(text):
        numbers = [int(digit) for digit in list(text[1:-1])]
        numbers[0] *= 2
        numbers[1] *= 7
        numbers[2] *= 6
        numbers[3] *= 5
        numbers[4] *= 4
        numbers[5] *= 3
        numbers[6] *= 2
        return sum(numbers)
