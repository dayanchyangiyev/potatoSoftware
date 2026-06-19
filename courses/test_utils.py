import unittest

from courses.utils import clamp, merge_sorted, parse_pair


class ClampTest(unittest.TestCase):
    def test_below_low_returns_low(self):
        self.assertEqual(clamp(-5, 0, 10), 0)

    def test_above_high_returns_high(self):
        self.assertEqual(clamp(15, 0, 10), 10)

    def test_within_range_returns_value(self):
        self.assertEqual(clamp(5, 0, 10), 5)

    def test_equal_to_bounds(self):
        self.assertEqual(clamp(0, 0, 10), 0)
        self.assertEqual(clamp(10, 0, 10), 10)

    def test_works_with_floats(self):
        self.assertEqual(clamp(2.5, 1.0, 2.0), 2.0)


class MergeSortedTest(unittest.TestCase):
    def test_interleaves_two_sorted_lists(self):
        self.assertEqual(merge_sorted([1, 3, 5], [2, 4, 6]), [1, 2, 3, 4, 5, 6])

    def test_both_empty(self):
        self.assertEqual(merge_sorted([], []), [])

    def test_one_empty(self):
        self.assertEqual(merge_sorted([], [1, 2, 3]), [1, 2, 3])
        self.assertEqual(merge_sorted([1, 2, 3], []), [1, 2, 3])

    def test_handles_duplicates_and_equal_elements(self):
        self.assertEqual(merge_sorted([1, 2, 2], [2, 3]), [1, 2, 2, 2, 3])

    def test_different_lengths(self):
        self.assertEqual(merge_sorted([1], [2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_result_is_sorted(self):
        a = [1, 4, 7, 9]
        b = [2, 3, 8]
        self.assertEqual(merge_sorted(a, b), sorted(a + b))


class ParsePairTest(unittest.TestCase):
    def test_valid_pair(self):
        self.assertEqual(parse_pair('3:4'), (3, 4))

    def test_negative_numbers(self):
        self.assertEqual(parse_pair('-1:-2'), (-1, -2))

    def test_returns_ints(self):
        a, b = parse_pair('10:20')
        self.assertIsInstance(a, int)
        self.assertIsInstance(b, int)

    def test_too_few_parts_raises(self):
        with self.assertRaises(ValueError):
            parse_pair('5')

    def test_too_many_parts_raises(self):
        with self.assertRaises(ValueError):
            parse_pair('1:2:3')

    def test_non_integer_raises(self):
        with self.assertRaises(ValueError):
            parse_pair('a:b')
