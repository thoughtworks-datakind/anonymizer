class AnalyzerResult:

    def __init__(self, text, entity_type, start, end):
        self.text = text
        self.entity_type = entity_type
        self.start = start
        self.end = end

    def __eq__(self, other):
        return type(self) == type(other) and self.text == other.text and self.entity_type == other.entity_type \
               and self.start == other.start and self.end == other.end
