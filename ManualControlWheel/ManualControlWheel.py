import turtle
from tkinter import *
from PIL import Image
from PIL import ImageTk

class ManualControlWheel:

    wheels_created = 0

    def __init__(self, canvas, root, title):
        t = turtle.RawTurtle(canvas)
        t.hideturtle()
        t.speed(0)
        t.pencolor("#000000")

        screen_dim_to_use = min(int(canvas['width']), int(canvas['height']))
        screen_dims = int(canvas['width']), int(canvas['height'])
        img_dim = int(screen_dim_to_use / 5)
        outer_circle_rad = screen_dim_to_use / 3.15
        inner_circle_rad = screen_dim_to_use / 2.15
        label_additional_height = int(screen_dims[0] / 20)

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

        img = img.resize((img_dim, img_dim), Image.ANTIALIAS)
        imgTk = ImageTk.PhotoImage(img)
        canvas.create_image((0, -outer_circle_rad - img_dim / 2), image=imgTk)
        ManualControlWheel.assign_image(root, imgTk)

        # Detect mouse clicked/dragged
        canvas.bind("<Button-1>", ManualControlWheel.mouse_clicked)
        canvas.bind("<B1-Motion>", ManualControlWheel.mouse_dragged)
        
    # Mouse clicked event
    @staticmethod
    def mouse_clicked(event):
        print("Clicked at", event.x, event.y)

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
