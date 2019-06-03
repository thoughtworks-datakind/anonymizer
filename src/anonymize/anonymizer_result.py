class AnonymizerResult:

    def __init__(self, redacted_text, analyzer_results):
        self.redacted_text = redacted_text
        self.analyzer_results = analyzer_results

    def __eq__(self, other):
        return type(self) == type(other) and self.redacted_text == other.redacted_text and self.analyzer_results == other.analyzer_results

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "PII information found: \n{}\nRedacted text: {}".format(self.analyzer_results, self.redacted_text)
