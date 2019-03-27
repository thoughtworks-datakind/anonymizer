from analyze.base_detector import BaseDetector
from analyze.regex import RegEx


class NRICDetector(BaseDetector):

    def __init__(self):
        self.name = "nric"
        self.pattern = RegEx().one_of("STFG").any_digit().num_occurrences(7).range("A", "Z").build()

    def validate(self, text):

        numbers = [int(digit) for digit in list(text[1:-1])]
        first_character = text[0]

        numbers[0] *= 2
        numbers[1] *= 7
        numbers[2] *= 6
        numbers[3] *= 5
        numbers[4] *= 4
        numbers[5] *= 3
        numbers[6] *= 2

        weight = sum(numbers)

        offset = 4 if first_character == "T" or first_character == "G" else 0
        loc = (offset + weight) % 11

        st = ["J", "Z", "I", "H", "G", "F", "E", "D", "C", "B", "A"]
        fg = ["X", "W", "U", "T", "R", "Q", "P", "N", "M", "L", "K"]

        if first_character == "S" or first_character == "T":
            expected_last_character = st[loc]
        else:
            if first_character == "F" or first_character == "G":
                expected_last_character = fg[loc]

        return expected_last_character == text[8]
