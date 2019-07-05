import turtle
from tkinter import *
from RoboticArmSimulator.Shape import Shape

class Rectangle(Shape):
    
    def __init__(self, origin, size, canvas, t, color):
        super(Rectangle, self).__init__(origin, size, canvas, t)
        if color == '':
            self.draw(origin, size)
        else:
            self.drawFill(origin, size, color)
        
    def drawFill(self, origin, size, color):
        t = self.getTurtle()
        t.penup()
        t.setx(origin.xPos - self.getCanvasSize().width / 2 + size.width)
        t.sety(origin.yPos - self.getCanvasSize().height / 2 + size.height)
        t.setheading(270)
        t.pendown()
        t.fillcolor(color)
        t.begin_fill()
        t.forward(size.height)
        t.left(-90)
        t.forward(size.width)
        t.left(-90)
        t.forward(size.height)
        t.left(-90)
        t.forward(size.width)
        t.end_fill()
        t.penup()
    
    def draw(self, origin, size):
        t = self.getTurtle()
        t.penup()
        t.setx(origin.xPos - self.getCanvasSize().width / 2 + size.width)
        t.sety(origin.yPos - self.getCanvasSize().height / 2 + size.height)
        t.setheading(270)
        t.pendown()
        t.forward(size.height)
        t.left(-90)
        t.forward(size.width)
        t.left(-90)
        t.forward(size.height)
        t.left(-90)
        t.forward(size.width)
        t.penup()