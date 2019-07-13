import math


class Point:
    
    """
    x - Position of x coordinate
    y - Position of y coordinate
    """
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def distance(p1, p2):
        return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
