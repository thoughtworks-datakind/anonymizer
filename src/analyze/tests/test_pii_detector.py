from unittest import TestCase
from analyze.pii_detector import PIIDetector


class TestPIIDetector(TestCase):

    def test_should_detect_nric_in_text(self):
        results = PIIDetector.analyze("First President of Singapore NRIC was S0000001I")
        self.assertEqual("The text S0000001I at position(38,47) was identified as NRIC", results[0])

    def test_should_detect_email_in_text(self):
        results = PIIDetector.analyze("A typical email id would look something like test@sample.com")
        self.assertEqual("The text test@sample.com at position(45,60) was identified as Email", results[0])

    def test_should_detect_nric_and_email_in_text(self):
        results = PIIDetector.analyze("""First President of Singapore NRIC was S0000001I.
                                         A typical email id would look something like test@sample.com""")

        self.assertEqual("The text S0000001I at position(38,47) was identified as NRIC", results[0])
        self.assertEqual("The text test@sample.com at position(135,150) was identified as Email", results[1])
