from src.analyze.national_id_detector import NationalIdDetector
from src.analyze.email_detector import EmailDetector
from src.analyze.phone_number_detector import PhoneNumberDetector

class PIIDetector:

    def __init__(self):
        pass

    @staticmethod
    def analyze(text):
        detectors = [NationalIdDetector(), EmailDetector(), PhoneNumberDetector()]
        return [match for detector in detectors for match in detector.execute(text)]

