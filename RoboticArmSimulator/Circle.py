import turtle
from tkinter import *
from RoboticArmSimulator.Shape import Shape
from RoboticArmSimulator.Size import Size
from RoboticArmSimulator.Point import Point

class Circle(Shape):
        
    def __init__(self, origin, radius, canvas, t, color):
        super(Circle, self).__init__(origin, Size(radius * 2, radius * 2), canvas, t)
        if color == "":
            self.draw(origin, radius)
        else:
            self.drawFill(origin, radius, color)
        
    def draw(self, origin, radius):
        t = self.getTurtle()
        t.penup()
        t.setx(origin.xPos - self.getCanvasSize().width / 2)
        t.sety(origin.yPos - self.getCanvasSize().height / 2)
        t.pendown()
        t.circle(radius)
        t.penup()
        
    def drawFill(self, origin, radius, color):
        t = self.getTurtle()
        t.penup()
        t.setx(origin.xPos - self.getCanvasSize().width / 2)
        t.sety(origin.yPos - self.getCanvasSize().height / 2)
        t.pendown()
        t.fillcolor(color)
        t.begin_fill()
        t.circle(radius)
        t.end_fill()
        t.penup()