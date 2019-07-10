from RoboticArmSimulator.Shape import Shape
from RoboticArmSimulator.Cartesian import Cartesian


class Rectangle(Shape):

    """
    Instance variables:
    __rotation - In degrees, the amount the shape has been rotated. Refreshes every 180 degrees for this shape
    """

    def __init__(self, origin, size, master_canvas, fill_color=None, border_color=None):
        self.__rotation = 0
        super(Rectangle, self).__init__(origin, size, master_canvas, fill_color, border_color)
        
    def draw(self, origin=None, size=None, rotation=None, fill_color=None):
        if origin is None:
            origin = self.get_origin()

        if size is None:
            size = self.get_size()

        if fill_color is None:
            fill_color = self.get_fill_color()

        if rotation is None:
            rotation = self.get_rotation()

        t = self.get_turtle()
        t.clear()
        t.penup()

        cartesian = Cartesian.computer_to_cartesian(origin, self.get_master_canvas())
        t.setx(cartesian.x - 3)
        t.sety(cartesian.y + 5)
        print(str(rotation))
        t.setheading(270 + rotation)

        t.pendown()
        
        if fill_color is not None:
            t.fillcolor(fill_color)
            t.begin_fill()

        t.forward(size.height)
        t.left(90)
        t.forward(size.width)
        t.left(90)
        t.forward(size.height)
        t.left(90)
        t.forward(size.width)
        
        if fill_color is not None:
            t.end_fill()
        
        t.penup()

    def contains(self, point):
        corners = self.get_frame_corners()
        if corners[0].x <= point.x <= corners[1].x and corners[0].y <= point.y <= corners[3].y:
            return True

        return False

    def get_rotation(self):
        return self.__rotation

    # Rotates around origin of rectangle
    def rotate(self, degrees):
        self.__rotation += degrees
        if self.__rotation >= 360:
            self.__rotation -= 360

        self.draw()
