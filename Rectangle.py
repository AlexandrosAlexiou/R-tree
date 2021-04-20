import math
from typing import List


class Rectangle:
    """
    Rectangle that represents an MBR
    """

    def __init__(self, x_low: float, x_high: float, y_low: float, y_high: float):
        self.x_low = x_low
        self.x_high = x_high
        self.y_low = y_low
        self.y_high = y_high

    def __eq__(self, other):
        if isinstance(other, Rectangle):
            return self.x_low == other.x_low \
                   and self.x_high == other.x_high \
                   and self.y_low == other.y_low \
                   and self.y_high == other.y_high
        return False

    def __str__(self):
        return f'{self.x_low}, {self.x_high}, {self.y_low}, {self.y_high}'

    @property
    def width(self):
        return self.x_high - self.x_low

    @property
    def height(self):
        return self.y_high - self.y_low

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

    def area(self) -> float:
        return self.width * self.height

    def centroid(self) -> (float, float):
        cx = (self.x_low + self.x_high) / 2
        cy = (self.y_low + self.y_high) / 2
        return cx, cy

    def intersects(self, other) -> bool:
        if isinstance(other, Rectangle):
            if (self.x_low >= other.x_high) or \
                    (self.x_high <= other.x_low) or \
                    (self.y_high <= other.y_low) or \
                    (self.y_low >= other.y_high):
                return False or self.inside(other) or other.inside(self) or self == other
            return True
        return False

    def inside(self, other) -> bool:
        if isinstance(other, Rectangle):
            inside_in_x_axis = (other.x_high >= self.x_high) and (other.x_low <= self.x_low)
            inside_in_y_axis = (other.y_low <= self.y_low) and (other.y_high >= self.y_high)
            return inside_in_x_axis and inside_in_y_axis
        return False

    def distance(self, point: (float, float)) -> float:
        """
        calculates the distance between an MBR and a point
        """
        x, y = point
        dx = self.x_low - x if x < self.x_low else 0 or x - self.x_high if x > self.x_high else 0
        dy = self.y_low - y if y < self.y_low else 0 or y - self.y_high if y > self.y_high else 0

        return math.sqrt(dx**2 + dy**2)


def calculate_MBR(coords: List[List]) -> Rectangle:
    """
    calculates the MBR of an object given the coordinates of its edges
    """
    x_low = min(coord[0] for coord in coords)
    x_high = max(coord[0] for coord in coords)
    y_low = min(coord[1] for coord in coords)
    y_high = max(coord[1] for coord in coords)
    return Rectangle(x_low, x_high, y_low, y_high)


def calculate_Geohash(mbr: Rectangle) -> int:
    try:
        import pymorton as pm
    except ImportError:
        raise RuntimeError("Please install pymorton to calculate geohashes: pip install pymorton")
    x, y = mbr.centroid()
    return pm.interleave_latlng(y, x)
