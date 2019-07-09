from RoboticArmSimulator.Shape import Shape
from RoboticArmSimulator.Size import Size


class Circle(Shape):
        
    """
    Instance variables:
    __radius - radius of the circle
    """
        
    def __init__(self, origin, radius, master_canvas, fill_color=None, border_color=None):
        self.__radius = radius
        super(Circle, self).__init__(origin, Size(radius * 2, radius * 2), master_canvas, fill_color, border_color)
        self.set_origin(origin)
        
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
        # t.setx(origin.xPos + self.getSize().width / 2)
        #t.sety(origin.yPos - self.getSize().height)
        t.setx(0)
        t.sety(-self.get_size().height / 2)
            
        t.pendown()
        
        if fill_color is not None:
            t.fillcolor(fill_color)
            t.begin_fill()
            
        t.circle(radius)
        
        if fill_color is not None:
            t.end_fill()
        
        t.penup()
        
    def draw_test_shape(self, radius=None, fill_color=None):
        t = self.get_test()
        t.clear()
        t.penup()
        origin = self.get_origin_cartesian()
            
        if radius is None:
            radius = self.get_radius()
            
        if fill_color is None:
            fill_color = self.get_fill_color()

        t.setx(origin.x)
        t.sety(origin.y)
            
        t.pendown()
        
        if fill_color is not None:
            t.fillcolor(fill_color)
            t.begin_fill()
            
        t.circle(radius)
        
        if fill_color is not None:
            t.end_fill()
        
        t.penup()
        
    def get_radius(self):
        return self.__radius
    
    def set_radius(self, radius):
        self.__radius = radius
        
    def set_size(self, size):
        self.__radius = size.width / 2
        super(Circle, self).set_size(size)
