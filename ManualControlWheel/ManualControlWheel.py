import turtle
from tkinter import *
from PIL import Image
from PIL import ImageTk
import math
from Ideas.shapes.Cartesian import Cartesian
from RoboticArmSimulator.Simulator import Simulator


class ManualControlWheel:

    wheels_created = 0

    """
    Class variables:
    wheels_created - Number of ManualControlWheel objects created during the current execution
    
    Instance variables: 
    canvas - Canvas of current ManualControlWheel
    total_theta - Total amount to rotate arrow by
    master - Tabcontrol view containing 
    
    img_dim - Dimension of arrow image
    center - Center of both circles
    number - The number of this instance
    
    curr_image - The TKImage object for this instance
    imgTk - Arrow image
    
    old_dim - Previous location of arrow in view
    """

    def __init__(self, canvas, root, title):
        self.canvas = canvas
        self.total_theta = 0
        self.master = root

        t = turtle.RawTurtle(canvas)
        t.hideturtle()
        t.speed(0)
        t.pencolor("#000000")

        screen_dim_to_use = min(float(canvas['width']), float(canvas['height']))
        screen_dims = float(canvas['width']), float(canvas['height'])
        self.img_dim = float(screen_dim_to_use / 5)
        outer_circle_rad = screen_dim_to_use / 3.15
        inner_circle_rad = screen_dim_to_use / 2.15
        label_additional_height = float(screen_dims[0] / 20)
        self.center = 0, 0

        #self.draw_axes_center(t)

        # Plot axes on graph using turtle
        #ManualControlWheel.draw_axes(t, screen_dims)

        t.penup()
        t.setx(0)
        t.sety(-outer_circle_rad + self.img_dim / 2)
        
        t.pendown()
        t.circle(outer_circle_rad - self.img_dim / 2)
        t.penup()
        
        t.sety(-inner_circle_rad + self.img_dim / 2)

        t.pendown()
        t.circle(inner_circle_rad - self.img_dim / 2)
        t.penup()

        canvas.create_text((0, (-screen_dims[1] / 2) + label_additional_height), text=title, width=100)

        ManualControlWheel.wheels_created += 1
        self.number = ManualControlWheel.wheels_created

        self.curr_image = Image.open("ManualControlWheel/ColorWheelArrow.png").convert("RGBA")

        self.curr_image = self.curr_image.resize((int(self.img_dim), int(self.img_dim)), Image.ANTIALIAS)
        self.imgTk = ImageTk.PhotoImage(self.curr_image)

        img_pos = 0, -outer_circle_rad - self.img_dim / 2

        fff = Image.new("RGBA", self.curr_image.size, (255, 255, 255, 0))
        out = Image.composite(self.curr_image, fff, self.curr_image)
        self.imgTk = ImageTk.PhotoImage(out)

        canvas.create_image((img_pos[0],
                             img_pos[1] - math.sin(90) * self.img_dim / 4),
                            image=self.imgTk, tags='image_tag', anchor="center")

        self.old_dim = img_pos
        self.assign_image(root, self.imgTk)

        """ Draws line at current arrow coordinate 
        t.penup()
        t.setx(canvas.coords('image_tag')[0])
        t.sety(-canvas.coords('image_tag')[1])
        t.pendown()
        t.forward(100)"""

        # Detect mouse clicked/dragged
        canvas.bind("<Button-1>", self.mouse_clicked)
        canvas.bind("<B1-Motion>", self.mouse_dragged)
        
    # Mouse clicked event
    def mouse_clicked(self, event):
        self.move_arrow(event)

        """ For testing purposes
        print("Distance from center is: ", center_distance)
        print("Clicked at", cartesian)
        print("Center at", self.center)
        print("Angle of", math.degrees(theta))
        print("Event at", event.x, event.y)
        print("\n")"""

    # Mouse dragged event
    def mouse_dragged(self, event):
        self.move_arrow(event)

    def assign_image(self, root, img):
        if self.number == 1:
            root.one = img
        elif self.number == 2:
            root.two = img
        elif self.number == 3:
            root.three = img
        elif self.number == 4:
            root.four = img
        elif self.number == 5:
            root.five = img
        else:
            print("Too many wheels created")

    def move_arrow(self, event):
        # (1) Get distance from center of circle to point where mouse was clicked
        cartesian = Cartesian.computer_to_cartesian((event.x, event.y), canvas=self.canvas)
        cartesian = cartesian[0] - 4.0, cartesian[1] + 5.0

        # (2) Calculate angle relative to y axis (0 is default position)
        if cartesian[0] != 0:
            theta = math.atan((cartesian[1] - self.center[1]) / cartesian[0])
        else:
            theta = 0

        if cartesian[0] < 0:
            theta += math.radians(180)
        elif cartesian[0] > 0:
            theta += math.radians(360)
        else:
            if cartesian[1] <= 0:
                theta += math.radians(270)
            else:
                theta += math.radians(90)

        if cartesian[1] == 0:
            if cartesian[0] <= 0:
                theta = math.radians(180)

        theta -= math.radians(90)
        theta = -theta

        curr_move = theta - self.total_theta

        # (3) Move arrow to theta and rotate arrow to appropriate location
        rot = self.curr_image.rotate(math.degrees(-theta), resample=Image.BICUBIC, expand=True)

        rot.convert("RGBA")
        fff = Image.new("RGBA", rot.size, (255, 255, 255, 0))
        out = Image.composite(rot, fff, rot)
        self.imgTk = ImageTk.PhotoImage(out)

        # center_distance = self.distance_from_center(self.old_dim)
        # print("Old dim:", self.old_dim)
        new_dim = Simulator.rotate(self.center, self.old_dim, curr_move)
        self.old_dim = new_dim
        # print("New dim:", new_dim)

        self.canvas.delete('image_tag')
        self.canvas.create_image((new_dim[0] + (math.cos(-theta + math.radians(90)) * self.img_dim / 4),
                                  new_dim[1] - (math.sin(-theta + math.radians(90)) * self.img_dim) / 4),
                                 image=self.imgTk, tags='image_tag', anchor="center")
        self.assign_image(self.master, self.imgTk)

        self.total_theta = theta

    @staticmethod
    def draw_axes(t, screen_dims):
        # y axis
        t.setx(0)
        t.sety(0)
        t.setheading(90)
        t.pendown()
        t.forward(screen_dims[1] / 2)
        t.penup()

        t.sety(0)
        t.setheading(-90)
        t.pendown()
        t.forward(screen_dims[1] / 2)
        t.penup()

        # x axis
        t.setx(0)
        t.sety(0)
        t.setheading(0)
        t.pendown()
        t.forward(screen_dims[0] / 2)
        t.penup()

        t.setx(0)
        t.sety(0)
        t.setheading(180)
        t.pendown()
        t.forward(screen_dims[0] / 2)
        t.penup()

        t.setx(0)
        t.sety(0)
        t.setheading(0)

    def draw_axes_center(self, t):
        t.penup()
        t.setx(0)
        t.sety(self.center[1])
        t.pendown()
        t.forward(100)
        t.penup()

    def distance_from_center(self, point):
        return math.sqrt((self.center[0] - point[0]) ** 2 + (self.center[1] - point[1]) ** 2)
