from unittest import TestCase
from analyze.pattern import Pattern


class TestPattern(TestCase):

    # Testing one_of
    def test_when_one_of_param_is_empty_throws_error(self):
        self.assertRaises(ValueError, lambda: Pattern().one_of("").build())
        self.assertRaises(ValueError, lambda: Pattern().one_of("A").build())

    def test_when_valid_input_is_passed_one_of_returns_correct_output(self):
        self.assertEqual("[AB]", Pattern().one_of("AB").build())
        self.assertEqual("[357]", Pattern().one_of("357").build())

    # Testing num_occurrences
    def test_when_non_positive_number_of_occurrences_throws_error(self):
        self.assertRaises(ValueError, lambda: Pattern().num_occurrences(-7).build())
        self.assertRaises(ValueError, lambda: Pattern().num_occurrences(0).build())

    def test_when_valid_input_is_passed_num_occurrences_returns_correct_output(self):
        self.assertEqual("{7}", Pattern().num_occurrences(7).build())

    # Testing any_digit
    def test_when_any_digit_returns_correct_output(self):
        self.assertEqual("\\d", Pattern().any_digit().build())

    # Testing range
    def test_when_invalid_input_for_range_throws_error(self):
        self.assertRaises(ValueError, lambda: Pattern().range("", "Z").build())
        self.assertRaises(ValueError, lambda: Pattern().range("0", "").build())
        self.assertRaises(ValueError, lambda: Pattern().range("01", "9").build())
        self.assertRaises(ValueError, lambda: Pattern().range("A", "YZ").build())
        self.assertRaises(ValueError, lambda: Pattern().range("B", "A").build())
        self.assertRaises(ValueError, lambda: Pattern().range("9", "0").build())

    def test_when_valid_input_is_passed_range_returns_correct_output(self):
        self.assertEqual("[A-Z]", Pattern().range("A", "Z").build())
        self.assertEqual("[0-9]", Pattern().range("0", "9").build())

    # Testing complex inputs
    def test_builds_correct_pattern_for_NRIC(self):
        self.assertEqual("[AIR]\\d{7}[A-Z]",
                         Pattern().one_of("AIR")
                         .any_digit()
                         .num_occurrences(7)
                         .range("A", "Z")
                         .build())
