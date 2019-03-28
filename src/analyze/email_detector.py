from analyze.base_detector import BaseDetector
from analyze.regex import RegEx


class EmailDetector(BaseDetector):

    def __init__(self):
        self.name = "Email"
        self.pattern = RegEx().one_of("a-zA-Z0-9_.+-").one_or_more_occurrences().literal("@").one_of("a-zA-Z0-9-")\
            .one_or_more_occurrences().literal("\\.").one_of("a-zA-Z0-9-.").one_or_more_occurrences().build()
