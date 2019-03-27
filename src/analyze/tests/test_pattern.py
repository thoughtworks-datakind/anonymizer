from unittest import TestCase
from analyze.pattern import Pattern


class TestPattern(TestCase):

    def test_when_one_of_param_is_empty_throws_error(self):
        self.assertRaises(ValueError, lambda: Pattern().one_of("").build())

    def test_when_non_positive_number_of_occurrences_throws_error(self):
        self.assertRaises(ValueError, lambda: Pattern().num_occurrences(-7).build())
        self.assertRaises(ValueError, lambda: Pattern().num_occurrences(0).build())

    def test_when_any_digit_returns_correct_output(self):
        self.assertEqual("\\d", Pattern().any_digit().build())

    def test_when_invalid_input_for_range_throws_error(self):
        self.assertRaises(ValueError, lambda: Pattern().range("", "Z").build())
        self.assertRaises(ValueError, lambda: Pattern().range("0", "").build())
        self.assertRaises(ValueError, lambda: Pattern().range("01", "9").build())
        self.assertRaises(ValueError, lambda: Pattern().range("A", "YZ").build())

    def test_builds_correct_pattern_for_NRIC(self):
        self.assertEqual("[AIR]\\d{7}[A-Z]",
                         Pattern().one_of("AIR")
                         .any_digit()
                         .num_occurrences(7)
                         .range("A", "Z")
                         .build())
