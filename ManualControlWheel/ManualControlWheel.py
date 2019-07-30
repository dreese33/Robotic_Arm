import turtle
from tkinter import *
from PIL import Image
from PIL import ImageTk
import math
from Ideas.shapes.Cartesian import Cartesian


class ManualControlWheel:

    wheels_created = 0

    """
    Instance variables: 
    center - Center of both circles
    canvas - Canvas of current ManualControlWheel
    
    Class variables:
    wheels_created - Number of ManualControlWheel objects created during the current execution
    """

    def __init__(self, canvas, root, title):
        self.canvas = canvas

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

        img = Image.open("ManualControlWheel/ColorWheelArrow.png")

        img = img.resize((int(img_dim), int(img_dim)), Image.ANTIALIAS)
        imgTk = ImageTk.PhotoImage(img)
        canvas.create_image((0, -outer_circle_rad - img_dim / 2), image=imgTk)
        ManualControlWheel.assign_image(root, imgTk)

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

        if cartesian[0] == 0:
            if cartesian[1] <= 0:
                theta += math.radians(270)
            else:
                theta += math.radians(90)

        if cartesian[1] == 0:
            if cartesian[0] <= 0:
                theta = math.radians(180)

        print("Distance from center is: ", center_distance)
        print("Clicked at", cartesian)
        print("Center at", self.center)
        print("Angle of", math.degrees(theta))
        print("Event at", event.x, event.y)

    # Mouse dragged event
    @staticmethod
    def mouse_dragged(event):
        print("Dragged to", event.x, event.y)

    @staticmethod
    def assign_image(root, img):
        if ManualControlWheel.wheels_created == 1:
            root.one = img
        elif ManualControlWheel.wheels_created == 2:
            root.two = img
        elif ManualControlWheel.wheels_created == 3:
            root.three = img
        elif ManualControlWheel.wheels_created == 4:
            root.four = img
        elif ManualControlWheel.wheels_created == 5:
            root.five = img
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
