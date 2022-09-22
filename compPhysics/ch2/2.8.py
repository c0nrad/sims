from numpy import array, array_equal

a = array([1, 2, 3, 4], int)
b = array([2, 4, 6, 8], int)

assert array_equal(b / a + 1, [3, 3, 3, 3])
assert array_equal(b / (a + 1), [1, 4 / 3, 6 / 4, 8 / 5])
assert array_equal(1 / a, [1, 0.5, 1 / 3, 1 / 4])
