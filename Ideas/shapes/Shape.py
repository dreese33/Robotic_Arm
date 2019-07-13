import turtle
from Ideas.shapes.Point import Point
from Ideas.shapes.Size import Size
import abc
import math


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
    __rotation - The number of degrees the shape is rotated from its original position
    __curr_distance - Current distance between center of shape and origin of shape
    __rotation_180 - Is the rotation over 180 degrees
    """

    def __init__(self, origin, size, master_canvas, fill_color=None, border_color=None):
        self.__rotation = 0
        self.__rotation_180 = False

        self.__size = size
        self.__origin = origin
        self.__center = Point(origin.x + size.width / 2, origin.y + size.height / 2)
        self.__fill_color = fill_color
        self.__border_color = border_color

        self._calculate_curr_distance()
        self.__turtle = Shape.setup_turtle(master_canvas)
        self.__master_canvas = master_canvas

        # Test code
        self.using_sin = False
        self.overX = False
        self.overY = False
        self.lastNonstopPoint = self.__origin
        self.lastlastNonstopPoint = None
        self.lastlastDegree = 0
        self.lastDegree = 0

        self.delay_necessary = 0

        self.previous_quadrant = 0

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

    def get_rotation(self):
        return self.__rotation

    def get_curr_distance(self):
        return self.__curr_distance

    def _get_rotation_180(self):
        return self.__rotation_180

    # Setters
    def setx(self, x):
        self.__origin = Point(x, self.__origin.y)
        self.__set_center()
        self._calculate_curr_distance()

    def sety(self, y):
        self.__origin = Point(self.__origin.x, y)
        self.__set_center()
        self._calculate_curr_distance()

    def set_origin(self, origin):
        self.__origin = origin
        self.__set_center()
        self._calculate_curr_distance()

    def set_size(self, size):
        self.__size = size
        self.__set_center()
        self._calculate_curr_distance()

    def set_width(self, width):
        self.__size = Size(width, self.__size.height)
        self.__set_center()
        self._calculate_curr_distance()

    def set_height(self, height):
        self.__size = Size(self.__size.width, height)
        self.__set_center()
        self._calculate_curr_distance()

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
        self._calculate_curr_distance()

    def __set_center(self):
        self.__center = Point(self.__origin.x + self.__size.width / 2, self.__origin.y + self.__size.height / 2)
        self.draw()
        self._calculate_curr_distance()

    def set_center(self, center):
        self.__origin = Point(center.x - self.__size.width / 2, center.y - self.__size.height / 2)
        self.__center = center
        self.draw()
        self._calculate_curr_distance()

    def get_frame_corners(self) -> []:
        return [self.__origin, Point(self.__origin.x + self.__size.width, self.__origin.y),
                Point(self.__origin.x + self.__size.width, self.__origin.y + self.__size.height),
                Point(self.__origin.x, self.__origin.y + self.__size.height)]

    # Rotates around origin of rectangle, does not apply to circle currently
    def rotate(self, degrees):
        self.__rotation += degrees
        if self.__rotation >= 360:
            self.__rotation -= 360

        self.draw()

    # Rotates around center of rectangle, does not apply to circle
    def rotate_center(self, degrees):

        if self.delay_necessary == 0:
            self.__rotation += degrees
            if self.__rotation >= 360:
                self.__rotation -= 360
                print("Rotation reached")
        else:
            self.delay_necessary -= 1

        self.__origin = self._calculate_origin(degrees)

        self.draw()

    def _calculate_origin(self, degrees):

        radius = self.__curr_distance
        shape_origin = Point(self.__origin.x - self.__center.x, self.__center.y - self.__origin.y)
        acos_value = shape_origin.x / radius
        asin_value = shape_origin.y / radius

        current_quadrant = Shape.get_current_quadrant(shape_origin)
        print("Quadrant " + str(current_quadrant))

        if self.previous_quadrant == 0:
            self.previous_quadrant = current_quadrant
            if current_quadrant == 1:
                self.overY = True
                self.overX = False
            elif current_quadrant == 2:
                self.overX = False
                self.overY = False
            elif current_quadrant == 3:
                self.overX = True
                self.overY = False
            elif current_quadrant == 4:
                self.overX = True
                self.overY = True

        if self.using_sin:
            theta = math.asin(asin_value)
        else:
            theta = math.acos(acos_value)

        print("asin: " + str(asin_value))
        print("acos: " + str(acos_value))
        print("Theta: " + str(math.degrees(theta)))

        # Modify this section!
        if self.overX and self.overY:
            print("Over")
            theta_new = theta + math.radians(degrees)
            final_y = math.sin(theta_new) * radius + self.__center.y
            final_x = math.cos(theta_new) * radius + self.__center.x
        elif self.overX:
            print("Under")
            # Modify this for initial direction
            theta_new = theta + math.radians(degrees)

            final_y = math.sin(theta_new) * radius + self.__center.y
            final_x = math.cos(theta_new) * radius + self.__center.x
        elif self.overY:
            print("Over1")
            # Modify this for initial direction
            theta_new = theta - math.radians(degrees)

            final_y = -math.sin(theta_new) * radius + self.__center.y
            final_x = math.cos(theta_new) * radius + self.__center.x
        else:
            print("Under2")
            # Modify this for initial direction
            theta_new = theta - math.radians(degrees)

            final_y = -math.sin(theta_new) * radius + self.__center.y
            final_x = math.cos(theta_new) * radius + self.__center.x

        final_pt = Point(final_x, final_y)

        if self.previous_quadrant == 1:
            if current_quadrant == 2:
                self.delay_necessary += 1
                self.overY = False
                final_pt = Point(self.lastlastNonstopPoint.x - 2 * radius * math.cos(self.lastlastDegree),
                                 self.lastlastNonstopPoint.y)
                print("1-2")
            elif current_quadrant == 3:
                self.delay_necessary += 1
                self.overX = True
                self.overY = False
                final_pt = Point(self.lastlastNonstopPoint.x + 2 * radius * math.cos(self.lastlastDegree),
                                 self.lastlastNonstopPoint.y - 2 * radius * math.sin(self.lastlastDegree))
                print("1-3")
            elif current_quadrant == 4:
                self.delay_necessary += 1
                self.overX = True
                final_pt = Point(self.lastlastNonstopPoint.x,
                                 self.lastlastNonstopPoint.y + 4 * radius * math.sin(self.lastlastDegree))
                print("1-4")
        elif self.previous_quadrant == 2:
            if current_quadrant == 1:
                self.delay_necessary += 1
                self.overY = True
                final_pt = Point(self.lastlastNonstopPoint.x - 2 * radius * math.cos(self.lastlastDegree),
                                 self.lastlastNonstopPoint.y)
                print("2-1")
            elif current_quadrant == 3:
                self.delay_necessary += 1
                self.overX = True
                final_pt = Point(self.lastlastNonstopPoint.x,
                                 self.lastlastNonstopPoint.y + 2 * radius * math.sin(self.lastlastDegree))
                print("2-3")
            elif current_quadrant == 4:
                self.delay_necessary += 1
                self.overX = True
                self.overY = True
                final_pt = Point(self.lastlastNonstopPoint.x - 2 * radius * math.cos(self.lastlastDegree),
                                 self.lastlastNonstopPoint.y - 2 * radius * math.sin(self.lastlastDegree))
                print("2-4")
        elif self.previous_quadrant == 3:
            if current_quadrant == 1:
                self.delay_necessary += 1
                self.overY = True
                self.overX = False
                final_pt = Point(self.lastlastNonstopPoint.x - 2 * radius * math.cos(self.lastlastDegree),
                                 self.lastlastNonstopPoint.y + 2 * radius * math.sin(self.lastlastDegree))
                print("3-1")
            elif current_quadrant == 2:
                self.delay_necessary += 1
                self.overX = False
                self.overY = False
                final_pt = Point(self.lastlastNonstopPoint.x,
                                 self.lastlastNonstopPoint.y - 2 * radius * math.sin(self.lastlastDegree))
                print("3-2")
            elif current_quadrant == 4:
                self.delay_necessary += 1
                self.overY = True
                final_pt = Point(self.lastlastNonstopPoint.x - 2 * radius * math.cos(self.lastlastDegree),
                                 self.lastlastNonstopPoint.y)
                print("3-4")
        elif self.previous_quadrant == 4:
            if current_quadrant == 1:
                self.delay_necessary += 1
                self.overX = False
                final_pt = Point(self.lastlastNonstopPoint.x,
                                 self.lastlastNonstopPoint.y - 2 * radius * math.sin(self.lastlastDegree))
                print("4-1")
            elif current_quadrant == 2:
                self.delay_necessary += 1
                self.overX = False
                self.overY = False
                final_pt = Point(self.lastlastNonstopPoint.x + 2 * radius * math.cos(self.lastlastDegree),
                                 self.lastlastNonstopPoint.y + 2 * radius * math.sin(self.lastlastDegree))
                print("4-2")
            elif current_quadrant == 3:
                self.delay_necessary += 1
                self.overY = False
                final_pt = Point(self.lastlastNonstopPoint.x - 2 * radius * math.cos(self.lastlastDegree),
                                 self.lastlastNonstopPoint.y)
                print("4-3")

        self.lastlastNonstopPoint = self.lastNonstopPoint
        self.lastNonstopPoint = final_pt

        self.lastlastDegree = self.lastDegree
        self.lastDegree = theta_new

        # Set over 180
        if self.overX:
            self.__previous_acos = asin_value
        else:
            self.__previous_acos = acos_value

        print("X: " + str(final_x))
        print("Y: " + str(final_y))
        print("Rotation: " + str(self.__rotation))

        self.previous_quadrant = current_quadrant

        return final_pt

    @staticmethod
    def get_current_quadrant(origin):
        if origin.x >= 0 and origin.y >= 0:
            return 1
        elif origin.x <= 0 <= origin.y:
            return 2
        elif origin.x <= 0 and origin.y <= 0:
            return 3
        else:
            print("Quad 4: ", origin.x, origin.y)
            return 4

    def _calculate_curr_distance(self):
        self.__curr_distance = Point.distance(self.get_origin(), self.get_center())
        print("distance " + str(self.__curr_distance))

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

    # Does the shape contain the specified point
    @abc.abstractmethod
    def contains(self, point) -> bool:
        return False
