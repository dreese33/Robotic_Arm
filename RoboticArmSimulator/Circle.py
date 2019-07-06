import turtle
from tkinter import *
from RoboticArmSimulator.Shape import Shape
from RoboticArmSimulator.Size import Size
from RoboticArmSimulator.Point import Point

class Circle(Shape):
        
    """
    Instance variables:
    __radius - radius of the circle
    """
        
    def __init__(self, origin, radius, canvas, t, fillColor = None, borderColor = None):
        self.__radius = radius
        super(Circle, self).__init__(origin, Size(radius * 2, radius * 2), canvas, t, fillColor, borderColor)
        self.setOrigin(origin)
        """
        if fillColor == None:
            self.draw(origin, radius)
        else:
            self.draw(origin, radius, fillColor)"""
            
        
    def draw(self, origin = None, radius = None, fillColor = None):
        if origin == None:
            origin = self.getOrigin()
            
        if radius == None:
            radius = self.getRadius()
            
        if fillColor == None:
            fillColor = self.getFillColor()
        
        t = self.getTurtle()
        t.clear()
        t.penup()
        t.setx(origin.xPos + self.getSize().width / 2)
        t.sety(origin.yPos - self.getSize().height)
            
        t.pendown()
        
        if fillColor != None:
            t.fillcolor(fillColor)
            t.begin_fill()
            
        t.circle(radius)
        
        if fillColor != None:
            t.end_fill()
        
        t.penup()
        
    def getRadius(self):
        return self.__radius
    
    def setRadius(self, radius):
        self.__radius = radius
        
    def setSize(self, size):
        self.__radius = size.width / 2
        super(Circle, self).setSize(size)