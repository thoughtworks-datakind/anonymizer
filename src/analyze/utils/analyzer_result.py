class AnalyzerResult:

    def __init__(self, text, type, start, end):
        self.text = text
        self.type = type
        self.start = start
        self.end = end

    def __eq__(self, other):
        return type(self) == type(other) and self.text == other.text and self.type == other.type \
               and self.start == other.start and self.end == other.end

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Text {} at position ({},{}) was identified as {}".format(self.text, self.start, self.end, self.type)

    def detector(self):
        return self.type
