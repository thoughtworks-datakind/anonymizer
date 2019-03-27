class BaseDetector:

    def __init__(self):
        self.name = "detector name"
        self.pattern = "regex pattern"

    def validate(self, text):
        return True
