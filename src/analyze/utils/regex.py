class RegEx:

    def __init__(self):
        self.regex_string = ""

    def __is_numeric(self, value):
        return isinstance(value, int)

    def __is_single_character_value(self, value):
        return len(str(value)) == 1

    def __validate_range(self, start, end):
        if start > end:
            raise ValueError("Range start should be less than end")

    def boundary(self):
        self.regex_string += "\\b"
        return self

    def pipe(self):
        self.regex_string += "|"
        return self

    def range(self, from_char, to_char):
        if not self.__is_single_character_value(from_char) or not self.__is_single_character_value(to_char):
            raise ValueError("Range boundaries should be single character")

        self.__validate_range(from_char, to_char)
        self.regex_string += "[{}-{}]".format(from_char, to_char)
        return self

    def one_of(self, character_set):
        if character_set is None or character_set == "":
            raise ValueError("Character Set should not be empty")

        self.regex_string += "[" + character_set + "]"
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
        self.regex_string += "{" + str(start) + "," + str(end) + "}"
        return self

    def literal(self, literal):
        self.regex_string += literal
        return self

    def build(self):
        return self.regex_string
