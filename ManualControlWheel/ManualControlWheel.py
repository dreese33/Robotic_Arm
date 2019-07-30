import turtle
from tkinter import *


class ManualControlWheel:

    wheels_created = 0

    def __init__(self, canvas, root, title):
        t = turtle.RawTurtle(canvas)
        t.hideturtle()
        t.speed(0)
        t.pencolor("#000000")
        
        screen_dim_to_use = min(int(canvas['width']), int(canvas['height']))
        
        t.penup()
        t.sety(-screen_dim_to_use / 3.5)
        
        t.pendown()
        t.circle(screen_dim_to_use / 3.5)
        t.penup()
        
        t.sety(-screen_dim_to_use / 2.15)

        t.pendown()
        t.circle(screen_dim_to_use / 2.15)
        t.penup()

        ManualControlWheel.wheels_created += 1

        img = PhotoImage(file="ManualControlWheel/ColorWheelArrow.png")
        canvas.create_image((0, 0), image=img)
        ManualControlWheel.assign_image(root, img)

        canvas.create_text((0, -50), text=title, width=100)

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
            print("One created")
            root.one = img
        elif ManualControlWheel.wheels_created == 2:
            print("Two created")
            root.two = img
        elif ManualControlWheel.wheels_created == 3:
            print("Three created")
            root.three = img
        elif ManualControlWheel.wheels_created == 4:
            print("Four created")
            root.four = img
        elif ManualControlWheel.wheels_created == 5:
            print("Five created")
            root.five = img
        else:
            print("Too many wheels created")

