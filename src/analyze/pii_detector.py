import re
from analyze.nric_detector import NRICDetector


class PIIDetector:

    def __init__(self):
        pass

    @staticmethod
    def analyze(text):
        results = []
        detectors = [NRICDetector()]

        for detector in detectors:
            matches = re.finditer(detector.pattern, text)
            for match in matches:
                start, end = match.span()
                matching_text = text[start:end]
                if not detector.validate(matching_text):
                    continue
                results.append("The text {} at position({},{}) was identified as {}".format(matching_text, start, end, detector.name))

        return results
