class Pattern:

    def __init__(self):
        self.regex_string = ""

    def range(self, from_char, to_char):
        self.regex_string += "[" + from_char + "-" + to_char + "]"

    def one_of(self, chars):
        self.regex_string += "[" + chars + "]"

    def any_digit(self):
        self.regex_string += "\\d"

    def num_occurrences(self, number):
        self.regex_string += "{" + number + "}"

    def build(self):
        return self.regex_string
