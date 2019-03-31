from abc import ABC, abstractmethod
import re
from src.analyze.analyzer_result import AnalyzerResult

class BaseDetector(ABC):

    def __init__(self):
        self.name = None
        self.pattern = None

    @abstractmethod
    def get_pattern(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

    def validate(self, input):
        return True

    def execute(self, input):
        results = []
        matches = re.finditer(self.get_pattern(), input)
        #TODO simplify this a bit more
        for match in matches:
            start, end = match.span()
            pattern_match = input[start:end]
            if self.validate(pattern_match):
                results.append(AnalyzerResult(pattern_match, self.get_name(), start, end))
        return results