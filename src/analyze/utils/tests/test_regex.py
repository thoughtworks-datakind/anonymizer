from unittest import TestCase

from src.analyze.utils.regex import RegEx


class TestRegEx(TestCase):

    # Testing one_of
    def test_when_one_of_param_is_empty_throws_error(self):
        self.assertRaises(ValueError, lambda: RegEx().one_of("").build())

    def test_when_valid_input_is_passed_one_of_returns_correct_output(self):
        self.assertEqual("[AB]", RegEx().one_of("AB").build())
        self.assertEqual("[357]", RegEx().one_of("357").build())

    # Testing num_occurrences
    def test_when_non_positive_number_of_occurrences_throws_error(self):
        self.assertRaises(ValueError, lambda: RegEx().num_occurrences(-7).build())
        self.assertRaises(ValueError, lambda: RegEx().num_occurrences(0).build())

    def test_when_valid_input_is_passed_num_occurrences_returns_correct_output(self):
        self.assertEqual("{7}", RegEx().num_occurrences(7).build())

    # Testing any_digit
    def test_when_any_digit_returns_correct_output(self):
        self.assertEqual("\\d", RegEx().any_digit().build())

    def __assert_value_error_is_raised(self, fn, msg):
        with self.assertRaises(ValueError) as ve:
            fn()
        self.assertEqual(str(ve.exception), msg)

    def __assert_type_error_is_raised(self, fn, msg):
        with self.assertRaises(TypeError) as ve:
            fn()
        self.assertEqual(str(ve.exception), msg)

    # Testing range
    def test_when_range_is_incomplete(self):
        single_character = "Range boundaries should be single character"
        self.__assert_value_error_is_raised(lambda: RegEx().range("", "Z").build(), single_character)
        self.__assert_value_error_is_raised(lambda: RegEx().range("0", "").build(), single_character)
        self.__assert_value_error_is_raised(lambda: RegEx().range("01", "9").build(), single_character)
        self.__assert_value_error_is_raised(lambda: RegEx().range("A", "YZ").build(), single_character)

    def test_when_invalid_range_boundaries_are_provided(self):
        less_than_end = "Range start should be less than end"
        self.__assert_value_error_is_raised(lambda: RegEx().range("B", "A").build(), less_than_end)
        self.__assert_value_error_is_raised(lambda: RegEx().range("9", "0").build(), less_than_end)

    def test_when_valid_input_is_passed_range_returns_correct_output(self):
        self.assertEqual("[A-Z]", RegEx().range("A", "Z").build())
        self.assertEqual("[0-9]", RegEx().range("0", "9").build())

    # Testing range_occurrences
    def test_when_invalid_numeric_range_boundaries_are_provided(self):
        less_than_end = "Range start should be less than end"
        self.__assert_value_error_is_raised(lambda: RegEx().range_occurrences(9, 0).build(), less_than_end)

    def test_when_invalid_input_for_range_occurrences_throws_error(self):
        range_should_be_integers = "Range should be integers"
        self.__assert_type_error_is_raised(lambda: RegEx().range_occurrences(1.2, 2).build(), range_should_be_integers)
        self.__assert_type_error_is_raised(lambda: RegEx().range_occurrences("A", 9).build(), range_should_be_integers)

    def test_when_valid_input_is_passed_range_occurrences_returns_correct_output(self):
        self.assertEqual("{0,9}", RegEx().range_occurrences(0, 9).build())

    # Testing one_or_more_occurrences
    def test_when_valid_input_is_passed_one_or_more_occurrences_returns_correct_output(self):
        self.assertEqual("+", RegEx().one_or_more_occurrences().build())

    # Testing zero_or_more_occurrences
    def test_when_valid_input_is_passed_zero_or_more_occurrences_returns_correct_output(self):
        self.assertEqual("*", RegEx().zero_or_more_occurrences().build())

    # Testing zero_or_one_occurrences
    def test_when_valid_input_is_passed_zero_or_one_occurrences_returns_correct_output(self):
        self.assertEqual("?", RegEx().zero_or_one_occurrences().build())

    # Testing literal
    def test_when_valid_input_is_passed_literal_returns_correct_output(self):
        self.assertEqual("@", RegEx().literal("@").build())

    # Testing boundary
    def test_boundary(self):
        self.assertEqual("\\b", RegEx().boundary().build())

    # Testing complex inputs
    def test_builds_correct_pattern_for_NRIC(self):
        self.assertEqual("[AIR]\\d{7}[A-Z]",
                         RegEx()
                         .one_of("AIR")
                         .any_digit()
                         .num_occurrences(7)
                         .range("A", "Z")
                         .build())

        self.assertEqual("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+",
                         RegEx()
                         .one_of("a-zA-Z0-9_.+-")
                         .one_or_more_occurrences()
                         .literal("@")
                         .one_of("a-zA-Z0-9-")
                         .one_or_more_occurrences()
                         .literal("\\.")
                         .one_of("a-zA-Z0-9-.")
                         .one_or_more_occurrences()
                         .build())
