from RoboticArmSimulator.Shape import Shape
from RoboticArmSimulator.Cartesian import Cartesian


class Rectangle(Shape):
    
    def __init__(self, origin, size, master_canvas, fill_color=None, border_color=None):
        super(Rectangle, self).__init__(origin, size, master_canvas, fill_color, border_color)
        
    def draw(self, origin=None, size=None, fill_color=None):
        if origin is None:
            origin = self.get_origin()

        if size is None:
            size = self.get_size()

        if fill_color is None:
            fill_color = self.get_fill_color()

        t = self.get_turtle()
        t.clear()
        t.penup()

        cartesian = Cartesian.computer_to_cartesian(origin, self.get_master_canvas())
        t.setx(cartesian.x + self.get_width() - 3)
        t.sety(cartesian.y + 6)
        print("Coord:" + " x: " + str(cartesian.x) + " y: " + str(cartesian.y))
        print(self.get_turtle().turtlesize()[0])
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

    def contains(self, point):
        corners = self.get_frame_corners()
        if corners[0].x <= point.x <= corners[1].x and corners[0].y <= point.y <= corners[3].y:
            return True

        return False
