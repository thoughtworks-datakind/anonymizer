
from src.analyze.detectors.base_detector import BaseDetector
from src.analyze.detectors.email_detector import EmailDetector
from src.analyze.detectors.national_id_detector import NationalIdDetector
from src.analyze.detectors.phone_number_detector import PhoneNumberDetector


class PIIDetector:

    def __init__(self):
        pass

    @staticmethod
    def analyze(text):
        print([cls.__name__ for cls in BaseDetector.__subclasses__()])
        detectors = [NationalIdDetector(), EmailDetector(), PhoneNumberDetector()]
        return [match for detector in detectors for match in detector.execute(text)]

