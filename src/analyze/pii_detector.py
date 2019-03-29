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
                matching_text = text[start:end]
                if not detector.validate(matching_text):
                    continue
                results.append(AnalyzerResult(matching_text, detector.name, start, end))

        return results
