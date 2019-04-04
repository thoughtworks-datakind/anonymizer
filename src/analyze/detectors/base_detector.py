import re
from abc import ABC, abstractmethod

from src.analyze.utils.analyzer_result import AnalyzerResult


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

    def validate(self, text):
        return True

    def execute(self, text):
        results = []
        matches = re.finditer(self.get_pattern(), text)
        for match in matches:
            matched_string = match.string[match.start(): match.end()]
            if self.validate(matched_string):
                results.append(AnalyzerResult(matched_string, self.get_name(), match.start(), match.end()))
        return results
