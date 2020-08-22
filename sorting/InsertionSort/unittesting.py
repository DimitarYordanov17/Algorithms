import unittest
from insertion_sort import InsertionSort


class TestInsertionSort(unittest.TestCase):
    """
    I'm testing my implementation of Insertion Sort Algorithm with Python's built-in sorting algorithm.
    """
    def test_positive_integers(self):
        my_list = InsertionSort([4, 10, 2, 3, 8, 10, 100, 5, 8, 0, 1, 101, 17])
        sorted_ll = list(sorted([4, 10, 2, 3, 8, 10, 100, 5, 8, 0, 1, 101, 17]))

        self.assertListEqual(sorted_ll, my_list.cleaned())

    def test_negative_integers(self):
        my_list = InsertionSort([-1, -2, -100, -66, -3, -1, -7, -200])
        sorted_ll = list(sorted([-1, -2, -100, -66, -3, -1, -7, -200]))

        self.assertListEqual(sorted_ll, my_list.cleaned())

    def test_mixed_integers(self):
        my_list = InsertionSort([5, 1, 10, 0, -2, 11, -3, 2, -100, 61, -176743, 163, -176742, 9])
        sorted_ll = list(sorted([5, 1, 10, 0, -2, 11, -3, 2, -100, 61, -176743, 163, -176742, 9]))

        self.assertListEqual(sorted_ll, my_list.cleaned())

    def test_float_numbers(self):
        my_list = InsertionSort([0.01, 0.1, 1.21, 1.20, -1.1])
        sorted_ll = list(sorted([0.01, 0.1, 1.21, 1.20, -1.1]))

        self.assertListEqual(sorted_ll, my_list.cleaned())


if __name__ == '__main__':
    unittest.main()