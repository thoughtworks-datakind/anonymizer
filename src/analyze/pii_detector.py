import re
from analyze.national_id_detector import NationalIdDetector
from analyze.email_detector import EmailDetector
from analyze.phone_number_detector import PhoneNumberDetector
from analyze.analyzer_result import AnalyzerResult


class PIIDetector:

    def __init__(self):
        pass

    @staticmethod
    def analyze(text):
        results = []
        detectors = [NationalIdDetector(), EmailDetector(), PhoneNumberDetector()]

        for detector in detectors:
            matches = re.finditer(detector.pattern, text)
            for match in matches:
                start, end = match.span()
                pattern_match = text[start:end]
                if detector.validate(pattern_match):
                    results.append(AnalyzerResult(pattern_match, detector.name, start, end))

        return results
