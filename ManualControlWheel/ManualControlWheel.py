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
    Instance variables: 
    center - Center of both circles
    canvas - Canvas of current ManualControlWheel
    total_theta - Total amount to rotate arrow by
    curr_image - The TKImage object for this instance
    curr_saved_img - Where the image is saved
    
    Class variables:
    wheels_created - Number of ManualControlWheel objects created during the current execution
    """

    def __init__(self, canvas, root, title):
        self.canvas = canvas
        self.total_theta = 0
        self.curr_saved_image = None

        t = turtle.RawTurtle(canvas)
        t.hideturtle()
        t.speed(0)
        t.pencolor("#000000")

        screen_dim_to_use = min(float(canvas['width']), float(canvas['height']))
        screen_dims = float(canvas['width']), float(canvas['height'])
        img_dim = float(screen_dim_to_use / 5)
        outer_circle_rad = screen_dim_to_use / 3.15
        inner_circle_rad = screen_dim_to_use / 2.15
        label_additional_height = float(screen_dims[0] / 20)
        self.center = 0, -outer_circle_rad - label_additional_height + img_dim / 2 + inner_circle_rad / 2
        self.draw_axes_center(t)

        # Plot axes on graph using turtle
        ManualControlWheel.drawAxes(t, screen_dims)

        t.sety(-outer_circle_rad - label_additional_height + img_dim / 2)
        
        t.pendown()
        t.circle(outer_circle_rad - img_dim / 2)
        t.penup()
        
        t.sety(-inner_circle_rad - label_additional_height + img_dim / 2)

        t.pendown()
        t.circle(inner_circle_rad - img_dim / 2)
        t.penup()

        canvas.create_text((0, (-screen_dims[1] / 2) + label_additional_height), text=title, width=100)

        ManualControlWheel.wheels_created += 1
        self.number = ManualControlWheel.wheels_created

        self.curr_image = Image.open("ManualControlWheel/ColorWheelArrow.png")

        self.curr_image = self.curr_image.resize((int(img_dim), int(img_dim)), Image.ANTIALIAS)
        self.imgTk = ImageTk.PhotoImage(self.curr_image)
        canvas.create_image((0, -outer_circle_rad - img_dim / 2), image=self.imgTk, tags='image_tag')
        self.assign_image(root, self.imgTk)

        # Detect mouse clicked/dragged
        canvas.bind("<Button-1>", self.mouse_clicked)
        canvas.bind("<B1-Motion>", ManualControlWheel.mouse_dragged)
        
    # Mouse clicked event
    def mouse_clicked(self, event):
        # (1) Get distance from center of circle to point where mouse was clicked
        cartesian = Cartesian.computer_to_cartesian((event.x, event.y), canvas=self.canvas)
        cartesian = cartesian[0] - 4.0, cartesian[1] + 5.0
        center_distance = self.distance_from_center(cartesian)

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
        new_arrow_point = Simulator.rotate(self.center, self.canvas.coords('image_tag'), curr_move)
        self.canvas.coords('image_tag', new_arrow_point)

        self.total_theta = theta

        print("Distance from center is: ", center_distance)
        print("Clicked at", cartesian)
        print("Center at", self.center)
        print("Angle of", math.degrees(theta))
        print("Event at", event.x, event.y)
        print("\n")

    # Mouse dragged event
    @staticmethod
    def mouse_dragged(event):
        print("Dragged to", event.x, event.y)

    def assign_image(self, root, img):
        if self.number == 1:
            self.curr_saved_image = root.one = img
        elif self.number == 2:
            self.curr_saved_image = root.two = img
        elif self.number == 3:
            self.curr_saved_image = root.three = img
        elif self.number == 4:
            self.curr_saved_image = root.four = img
        elif self.number == 5:
            self.curr_saved_image = root.five = img
        else:
            print("Too many wheels created")

    @staticmethod
    def drawAxes(t, screen_dims):
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
