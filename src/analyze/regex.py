class RegEx:

    def __init__(self):
        self.regex_string = ""

    def __is_numeric(self, input):
        return isinstance(input, int)

    def __is_single_character_value(self, input):
        return len(input) == 1

    def __validate_range(self, start, end):
        if start > end:
            raise ValueError("Range start should be less than end")

    def range(self, from_char, to_char):
        if not self.__is_single_character_value(from_char) or not self.__is_single_character_value(to_char):
            raise ValueError("Range boundaries should be single character")

        self.__validate_range(from_char, to_char)
        self.regex_string += "[" + from_char + "-" + to_char + "]"
        return self

    def one_of(self, chars):
        if chars is None or len(chars) <= 1:
            raise ValueError("")

        self.regex_string += "[" + chars + "]"
        return self

    def any_digit(self):
        self.regex_string += "\\d"
        return self

    def num_occurrences(self, number):
        if number < 1:
            raise ValueError

        self.regex_string += "{" + str(number) + "}"
        return self

    def one_or_more_occurrences(self):
        self.regex_string += "+"
        return self

    def zero_or_more_occurrences(self):
        self.regex_string += "*"
        return self

    def zero_or_one_occurrences(self):
        self.regex_string += "?"
        return self

    def range_occurrences(self, start, end):
        if not self.__is_numeric(start) or not self.__is_numeric(end):
            raise TypeError("Range should be integers")

        self.__validate_range(start, end)
        self.regex_string += "{" + str(start) + "-" + str(end) + "}"
        return self

    def literal(self, literal):
        self.regex_string += literal
        return self

    def build(self):
        return self.regex_string
