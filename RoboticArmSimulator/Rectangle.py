from RoboticArmSimulator.Shape import Shape
from RoboticArmSimulator.Cartesian import Cartesian


class Rectangle(Shape):
    
    def __init__(self, origin, size, master_canvas, fill_color=None, border_color=None):
        super(Rectangle, self).__init__(origin, size, master_canvas, fill_color, border_color)
        
    def draw(self, origin=None, size=None, fill_color=None, border_color=None):
        t = self.get_turtle()
        t.clear()
        t.penup()
        
        if origin is None:
            origin = self.get_origin()
            
        if size is None:
            size = self.get_size()
            
        if fill_color is None:
            fill_color = self.get_fill_color()

        cartesian = Cartesian.computer_to_cartesian(origin, self.get_width(), self.get_master_canvas())
        t.setx(cartesian.x)
        t.sety(cartesian.y)
        t.setheading(270)
        t.pendown()
        
        if fill_color is not None:
            t.fillcolor(fill_color)
            t.begin_fill()
            
        t.forward(size.height)
        t.left(-90)
        t.forward(size.width)
        t.left(-90)
        t.forward(size.height)
        t.left(-90)
        t.forward(size.width)
        
        if fill_color is not None:
            t.end_fill()
        
        t.penup()

    """
    def draw_test_shape(self, origin=None, size=None, fill_color=None, border_color=None):
        t = self.get_test()
        t.clear()
        t.penup()
        
        origin = self.get_origin_cartesian()
            
        if size is None:
            size = self.get_size()
            
        if fill_color is None:
            fill_color = self.get_fill_color()
        
        t.setx(origin.x)
        t.sety(origin.y + self.get_master_canvas_size().height / 2 - self.get_size().height / 2)
        t.setheading(270)
        t.pendown()
        
        if fill_color is not None:
            t.fillcolor(fill_color)
            t.begin_fill()
            
        t.forward(size.height)
        t.left(-90)
        t.forward(size.width)
        t.left(-90)
        t.forward(size.height)
        t.left(-90)
        t.forward(size.width)
        
        if fill_color is not None:
            t.end_fill()
        
        t.penup()
    """

