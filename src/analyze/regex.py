class RegEx:

    def __init__(self):
        self.regex_string = ""

    def range(self, from_char, to_char):
        if len(from_char) != 1 or len(to_char) != 1 or from_char > to_char:
            raise ValueError

        self.regex_string += "[" + from_char + "-" + to_char + "]"
        return self

    def one_of(self, chars):
        if chars is None or len(chars) <= 1:
            raise ValueError

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

    def literal(self, literal):
        self.regex_string += literal
        return self

    def build(self):
        return self.regex_string
