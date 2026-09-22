import random
import unittest

from backend import sortowanie


class SortowanieTests(unittest.TestCase):
    def test_data_lifecycle(self):
        sorter = sortowanie()

        self.assertEqual(sorter.get_data(), [])
        sorter.add(4)
        sorter.add(-2)
        self.assertEqual(sorter.get_data(), [4, -2])

        sorter.clear()
        self.assertEqual(sorter.get_data(), [])

    def test_generate_data_has_requested_shape_and_bounds(self):
        random.seed(7)
        values = sortowanie().generate_data(-3, 5, 40)

        self.assertEqual(len(values), 40)
        self.assertTrue(all(-3 <= value <= 5 for value in values))

    def test_each_algorithm_sorts_duplicates_negative_values_and_empty_data(self):
        input_data = [5, -1, 5, 0, -10, 3, 0]
        expected = sorted(input_data)

        for algorithm_name in (
            "bubble_sort",
            "quick_sort",
            "insertion_sort",
            "selection_sort",
        ):
            with self.subTest(algorithm=algorithm_name):
                sorter = sortowanie()
                algorithm = getattr(sorter, algorithm_name)

                self.assertEqual(algorithm(input_data), expected)
                self.assertEqual(algorithm([]), [])

    def test_sorting_without_an_argument_uses_stored_data(self):
        sorter = sortowanie()
        sorter.data = [3, 1, 2]

        self.assertEqual(sorter.insertion_sort(), [1, 2, 3])
        self.assertEqual(sorter.get_data(), [1, 2, 3])


if __name__ == "__main__":
    unittest.main()