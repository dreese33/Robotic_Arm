from tkinter import *
import turtle
from RoboticArmSimulator.Point import Point
from RoboticArmSimulator.Size import Size
import abc


# Requires modification for setter methods to work
# Based on computer coordinate system primarily (the one used in tkinters Canvas)
# Also contains conversion to cartesian coordinate system (the one used by turtle)
class Shape(object):
    
    """
    __cartesian_origin - Initial point of shape, stored in cartesian coordinate system
    __computer_origin - Initial point of shape, stored in computer coordinate system
    __size - Width and height of shape (width, height)
    __canvas - Canvas shape is being drawn on
    __master_canvas - Canvas holding the primary canvas
    __turtle - Turtle drawing the shape
    __canvas_size - Size of the canvas
    __master_canvas_size - Dimension of the master canvas
    __fill_color - Color to fill Shape with, no fill if None
    __border_color - Color for border of shape
    __test - TEST
    """

    """
    def __init__(self, origin, size, master_canvas, fill_color=None, border_color=None):
        self.__master_canvas = master_canvas
        self.__canvas = Canvas(master=master_canvas, width=size.width, height=size.height, bd=0, highlightthickness=0)
        self.__canvas_size = Size(int(self.__canvas['width']), int(self.__canvas['height']))
        
        self.__size = size
        self.__computer_origin = origin
        
        if origin.y == 0:
            self.__cartesian_origin = Point(origin.x - self.__canvas_size.width / 2,
                                            origin.y - self.__canvas_size.height / 2)
        else:
            self.__cartesian_origin = Point(origin.x - self.__canvas_size.width / 2,
                                            self.__canvas_size.height / 2 - origin.y)
        
        self.__master_canvas_size = Size(int(master_canvas['width']), int(master_canvas['height']))
        self.__canvas.place(relx=origin.x / self.__master_canvas_size.width,
                            rely=origin.y / self.__master_canvas_size.height)
        
        self.__fill_color = fill_color
        self.__border_color = border_color
        
        # Setup turtle
        self.__turtle = Shape.setup_turtle(self, self.__canvas)
        self.draw()
        
        self.__test = Shape.setup_turtle(self, self.__master_canvas)
        self.__test._tracer(0)
        #self.drawTestShape()
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
    """
    def get_test(self):
        return self.__test
    
    def get_master_canvas_size(self):
        return self.__master_canvas_size
    
    def get_master_canvas(self):
        return self.__master_canvas
        
    def get_canvas_size(self):
        return self.__canvas_size
    """

    """
    def get_center(self):
        return Point(self.__size.width / 2 + self.__computer_origin.x,
                     self.__size.height / 2 + self.__computer_origin.y)
    
    def get_center_cartesian(self):
        return Point(self.__size.width / 2 + self.__cartesian_origin.x,
                     self.__size.height / 2 + self.__cartesian_origin.y)
    """

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


    """
    def get_origin(self):
        return self.__computer_origin
    
    def get_origin_cartesian(self):
        return self.__cartesian_origin
    """

    """
    def get_parent(self):
        return self.__canvas
    """
    
    # Setters
    def setx(self, x):
        self.__origin = Point(x, self.__origin.y)
        self.set_center()

    def sety(self, y):
        self.__origin = Point(self.__origin.x, y)
        self.set_center()

    def set_origin(self, origin):
        self.__origin = origin
        self.set_center()

    def set_size(self, size):
        self.__size = size
        self.set_center()

    def set_width(self, width):
        self.__size = Size(width, self.__size.height)
        self.set_center()

    def set_height(self, height):
        self.__size = Size(self.__size.width, height)
        self.set_center()

    def set_fill_color(self, fill_color):
        self.__fill_color = fill_color
        self.draw()

    def set_border_color(self, border_color):
        self.__border_color = border_color
        self.draw()

    def set_master_canvas(self, master_canvas):
        self.__turtle = Shape.setup_turtle(master_canvas)
        self.draw()

    def set_turtle(self, t):
        self.__turtle = t
        self.draw()

    def set_center(self):
        self.__center = Point(self.__origin.x + self.__size.width / 2, self.__origin.y + self.__size.height / 2)
        self.draw()

    """
    def set_origin_test(self, origin):
        self.__computer_origin = origin
        if origin.y == 0:
            self.__cartesian_origin = Point(origin.x - self.__canvas_size.width / 2,
                                            origin.y - self.__canvas_size.height / 2)
        else:
            self.__cartesian_origin = Point(origin.x - self.__canvas_size.width / 2,
                                            self.__canvas_size.height / 2 - origin.y)
        self.draw_test_shape()
    
        
    # Tested
    def set_origin(self, origin):
        self.__computer_origin = origin
        if origin.y == 0:
            self.__cartesian_origin = Point(origin.x - self.__canvas_size.width / 2,
                                            origin.y - self.__canvas_size.height / 2)
        else:
            self.__cartesian_origin = Point(origin.x - self.__canvas_size.width / 2,
                                            self.__canvas_size.height / 2 - origin.y)
        self.__canvas.place(relx=origin.x / self.__master_canvas_size.width,
                            rely=origin.y / self.__master_canvas_size.height)
    
        
    # Tested
    def set_center(self, center):
        originx = center.x - self.__size.width / 2
        if center.y >= 0:
            originy = center.y - self.__size.height / 2
        else:
            originy = center.y + self.__size.height / 2
        self.set_origin(Point(originx, originy))
        
    # Tested
    def setx(self, x):
        self.__cartesian_origin = Point(x - self.__canvas_size.width / 2, self.__cartesian_origin.y)
        self.__computer_origin = Point(x, self.__computer_origin.y)
        self.__canvas.place(relx=self.__computer_origin.x / self.__master_canvas_size.width,
                            rely=self.__computer_origin.y / self.__master_canvas_size.height)
        
    # Tested
    def sety(self, y):
        self.__computer_origin = Point(self.__computer_origin.x, y)
        if y == 0:
            self.__cartesian_origin = Point(self.__cartesian_origin.x, y - self.__canvas_size.height / 2)
        else:
            self.__cartesian_origin = Point(self.__cartesian_origin.x, self.__canvas_size.height / 2 - y)
        self.__canvas.place(relx=self.__computer_origin.x / self.__master_canvas_size.width,
                          rely=self.__computer_origin.y / self.__master_canvas_size.height)
    """


    """
    # Tested
    def set_center_x(self, x):
        self.__computer_origin = Point(x - self.__size.width / 2, self.__computer_origin.y)
        self.__cartesian_origin = Point(x - self.__size.width / 2, self.__cartesian_origin.y)
        self.__canvas.place(relx=self.__computer_origin.x / self.__master_canvas_size.width,
                            rely=self.__computer_origin.y / self.__master_canvas_size.height)
        
    # Tested
    def set_center_y(self, y):
        if y >= 0:
            originy = y - self.__size.height / 2
        else:
            originy = y + self.__size.height / 2
        
        computer_origin = Point(self.__computer_origin.x, originy)
        self.set_origin(computer_origin)
    """

    """
    def reset_shape(self, origin, size):
        self.set_size(size)
        self.set_origin(origin)
    """
        
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
