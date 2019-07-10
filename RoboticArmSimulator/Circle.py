from RoboticArmSimulator.Shape import Shape
from RoboticArmSimulator.Size import Size
from RoboticArmSimulator.Cartesian import Cartesian
import math


class Circle(Shape):
        
    """
    Instance variables:
    __radius - radius of the circle
    """
        
    def __init__(self, origin, radius, master_canvas, fill_color=None, border_color=None):
        self.__radius = radius
        super(Circle, self).__init__(origin, Size(radius * 2, radius * 2), master_canvas, fill_color, border_color)
        self.set_size(radius)
        
    def draw(self, origin=None, radius=None, fill_color=None):
        if origin is None:
            origin = self.get_origin()
            
        if radius is None:
            radius = self.get_radius()
            
        if fill_color is None:
            fill_color = self.get_fill_color()
        
        t = self.get_turtle()
        t.clear()
        t.penup()

        cartesian = Cartesian.computer_to_cartesian(origin, self.get_master_canvas())
        t.setx(cartesian.x + self.get_width() / 2 - 3)
        t.sety(cartesian.y - self.get_height() + 5)

        t.pendown()
        
        if fill_color is not None:
            t.fillcolor(fill_color)
            t.begin_fill()
            
        t.circle(radius)
        
        if fill_color is not None:
            t.end_fill()
        
        t.penup()

    def set_radius(self, radius):
        self.set_size(radius)

    def get_radius(self):
        return self.__radius

    def set_size(self, radius):
        self.__radius = radius
        super(Circle, self).set_size(Size(radius * 2, radius * 2))

    def contains(self, point):
        distance = math.sqrt((point.x - self.get_center().x) ** 2 + (point.y - self.get_center().y) ** 2)
        if distance <= self.__radius:
            return True

        return False
