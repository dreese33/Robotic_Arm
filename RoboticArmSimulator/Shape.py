import turtle
from RoboticArmSimulator.Point import Point
from RoboticArmSimulator.Size import Size
import abc


# Requires modification for setter methods to work
# Based on computer coordinate system primarily (the one used in tkinters Canvas)
# Also contains conversion to cartesian coordinate system (the one used by turtle)
class Shape(object):
    
    """
    __size - The size of the shape
    __origin - The origin of the shape
    __center - The center point of the shape
    __fill_color - The color to fill the shape with, if None, not filled
    __border_color - Default is black, the color of the border of the Shape
    __turtle - The turtle that draws the shape
    __master_canvas - The canvas the shape is in
    """

    def __init__(self, origin, size, master_canvas, fill_color=None, border_color=None):
        self.__size = size
        self.__origin = origin
        self.__center = Point(origin.x + size.width / 2, origin.y + size.height / 2)
        self.__fill_color = fill_color
        self.__border_color = border_color

        self.__turtle = Shape.setup_turtle(master_canvas)
        self.__master_canvas = master_canvas
        self.draw()

    # Getters
    def get_width(self):
        return self.__size.width

    def get_height(self):
        return self.__size.height

    def get_size(self):
        return self.__size

    def getx(self):
        return self.__origin.x

    def gety(self):
        return self.__origin.y

    def get_origin(self):
        return self.__origin

    def get_center(self):
        return self.__center

    def get_fill_color(self):
        return self.__fill_color

    def get_border_color(self):
        return self.__border_color

    def get_turtle(self):
        return self.__turtle

    def get_master_canvas(self):
        return self.__master_canvas
    
    # Setters
    def setx(self, x):
        self.__origin = Point(x, self.__origin.y)
        self.__set_center()

    def sety(self, y):
        self.__origin = Point(self.__origin.x, y)
        self.__set_center()

    def set_origin(self, origin):
        self.__origin = origin
        self.__set_center()

    def set_size(self, size):
        self.__size = size
        self.__set_center()

    def set_width(self, width):
        self.__size = Size(width, self.__size.height)
        self.__set_center()

    def set_height(self, height):
        self.__size = Size(self.__size.width, height)
        self.__set_center()

    def set_fill_color(self, fill_color):
        self.__fill_color = fill_color
        self.draw()

    def set_border_color(self, border_color):
        self.__border_color = border_color
        self.draw()

    def set_master_canvas(self, master_canvas):
        self.__turtle = Shape.setup_turtle(master_canvas)
        self.__master_canvas = master_canvas
        self.draw()

    def __set_center(self):
        self.__center = Point(self.__origin.x + self.__size.width / 2, self.__origin.y + self.__size.height / 2)
        self.draw()

    def set_center(self, center):
        self.__origin = Point(center.x - self.__size.width / 2, center.y - self.__size.height / 2)
        self.__center = center
        self.draw()

    # Setup non animated turtle
    @staticmethod
    def setup_turtle(master_canvas):
        t = turtle.RawTurtle(master_canvas)
        t._tracer(0)
        t.speed(0)
        t.hideturtle()
        t.penup()
        return t
        
    # Use these to set the values in the setters
    @abc.abstractmethod
    def draw(self):
        return
