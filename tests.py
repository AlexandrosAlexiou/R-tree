#!/usr/bin/env python3

import math
import unittest

from Rectangle import Rectangle


class TestRectangle(unittest.TestCase):
    """Rectangle class tests"""

    def test_init(self):
        """Basic test ensuring a Rect can be instantiated"""
        r = Rectangle(0, 1, 5, 9)
        self.assertEqual(0, r.x_low)
        self.assertEqual(1, r.x_high)
        self.assertEqual(5, r.y_low)
        self.assertEqual(9, r.y_high)

    def test_equals(self):
        """Basic test ensuring that two Rectangles are equal"""
        r1 = Rectangle(0, 1, 5, 9)
        r2 = Rectangle(0, 1, 5, 9)
        self.assertTrue(r1 == r2)

    def test_centroid(self):
        """Basic test ensuring that the centroid is calculated correctly"""
        r1 = Rectangle(0, 1, 5, 9)
        self.assertEqual((0.5, 7), r1.centroid())

    def test_intersection(self):
        """Basic test ensuring that two rectangles intersect"""
        r1 = Rectangle(0, 2, 0, 2)
        r2 = Rectangle(1, 1.5, 1, 1.5)
        self.assertTrue(r1.intersects(r2))

    def test_inside(self):
        """Basic test ensuring that two rectangles are inside one another"""
        r1 = Rectangle(0, 2, 0, 2)
        r2 = Rectangle(1, 1.5, 1, 1.5)
        self.assertTrue(not r1.inside(r2))
        self.assertTrue(r2.inside(r1))

    def test_distance(self):
        """Basic test ensuring that the distance of a point from a rectangle is calculated correctly"""
        r1 = Rectangle(0, 2, 0, 2)
        point1 = (3, 1)
        point2 = (3, 3)
        self.assertEqual(1.0, r1.distance(point1))
        self.assertEqual(math.sqrt(2), r1.distance(point2))


class TestMBR(unittest.TestCase):
    """MBR tests"""
    def test_calculation(self):
        """Basic test ensuring an MBR is calculated correctly"""
        from Rectangle import calculate_MBR
        coords = [[3.0, 4.0], [2.1, 3.5], [1.1, 10.123], [5.5, 9.534], [4.62, 0.65]]
        self.assertEqual(Rectangle(x_low=1.1, x_high=5.5, y_low=0.65, y_high=10.123), calculate_MBR(coords))


if __name__ == '__main__':
    unittest.main()
