class Pattern:

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

    def build(self):
        return self.regex_string
