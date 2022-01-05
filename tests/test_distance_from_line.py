import unittest

from altitude_generator import calculate_height


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.p1 = (5, 5)
        self.p2 = (10, 10)
        self.p3 = (4, 4)

        self.p4 = (0, 0)
        self.p5 = (0, 2)
        self.p6 = (0, 3)

        self.p7 = (0, 0)
        self.p8 = (4, 0)
        self.p9 = (2, 1)

        self.p10 = (10, 10)
        self.p11 = (20, 20)
        self.p12 = (6, 7)
        self.p13 = (18, 12)

    def test_something(self):
        distance = int(calculate_height((self.p1, self.p2), self.p3))
        self.assertEqual(distance, 1)  # add assertion here

    def test_vertical(self):
        distance = int(calculate_height((self.p4, self.p5), self.p6))
        self.assertEqual(distance, 1)

    def test_middle(self):
        distance = int(calculate_height((self.p7, self.p8), self.p9))
        self.assertEqual(distance, 1)

    def test_pitagorian_out(self):
        distance = int(calculate_height((self.p10, self.p11), self.p12))
        self.assertEqual(distance, 5)

    def test_pitagorian_in(self):
        distance = int(calculate_height((self.p10, self.p11), self.p13))
        self.assertEqual(distance, 4)


if __name__ == '__main__':
    unittest.main()
