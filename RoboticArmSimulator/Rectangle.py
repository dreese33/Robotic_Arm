import turtle
from tkinter import *
from RoboticArmSimulator.Shape import Shape

class Rectangle(Shape):
    
    def __init__(self, origin, size, canvas, t, fillColor = None, borderColor = None):
        super(Rectangle, self).__init__(origin, size, canvas, t, fillColor, borderColor)
        self.setOrigin(origin)
        """
        if fillColor == None:
            self.draw(origin, size)
        else:
            self.draw(origin, size, fillColor)"""
        
    def draw(self, origin = None, size = None, fillColor = None, borderColor = None):
        if origin == None:
            origin = self.getOrigin()
            
        if size == None:
            size = self.getSize()
            
        if fillColor == None:
            fillColor = self.getFillColor()
        
        t = self.getTurtle()
        t.clear()
        t.penup()
        t.setx(origin.xPos + size.width)
        t.sety(origin.yPos)
        t.setheading(270)
        t.pendown()
        
        if fillColor != None:
            t.fillcolor(fillColor)
            t.begin_fill()
            
        t.forward(size.height)
        t.left(-90)
        t.forward(size.width)
        t.left(-90)
        t.forward(size.height)
        t.left(-90)
        t.forward(size.width)
        
        if fillColor != None:
            t.end_fill()
        
        t.penup()