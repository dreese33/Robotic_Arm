from tkinter import *
from RoboticArmSimulator.Point import Point
from RoboticArmSimulator.Size import Size
import abc

#Requires modification for setter methods to work
class Shape(object):
    
    """
    __origin - Initial point of shape, stored in cartesian coordinate system
    __size - Width and height of shape (width, height)
    __canvas - Canvas shape is being drawn on
    __turtle - Turtle drawing the shape
    __canvasSize - Size of the canvas
    __fillColor - Color to fill Shape with, no fill if None
    __borderColor - Color for border of shape
    """
    
    def __init__(self, origin, size, canvas, t, fillColor = None, borderColor = None):
        self.__size = size
        self.__origin = origin
        self.__canvas = canvas
        self.__turtle = t
        self.__canvasSize = Size(int(canvas['width']), int(canvas['height']))
        self.__fillColor = fillColor
        self.__borderColor = borderColor
        
        #Setup turtle
        Shape.setup_turtle(self, canvas, t)
      
    #Getters
    #Tested
    def getCanvasSize(self):
        return self.__canvasSize
    
    def getCenter(self):
        return Point(self.__size.width / 2 + self.__origin.xPos, self.__size.height / 2 + self.__origin.yPos)
    
    #Tested
    def getSize(self):
        return self.__size
    
    def getOrigin(self):
        return self.__origin
    
    def getParent(self):
        return self.__canvas
    
    def getTurtle(self):
        return self.__turtle
    
    def getFillColor(self):
        return self.__fillColor
    
    def getBorderColor(self):
        return self.__borderColor
    
    #Setters
    #Tested
    def setSize(self, size):
        self.__size = size
        self.draw()
        
    #Tested
    def setOrigin(self, origin):
        if origin.yPos == 0:
            self.__origin = Point(origin.xPos - self.__canvasSize.width / 2, origin.yPos - self.__canvasSize.height / 2) 
        else:
            self.__origin = Point(origin.xPos - self.__canvasSize.width / 2, self.__canvasSize.height / 2 - origin.yPos)
        self.draw()
        
    def setCenter(self, center):
        originXPos = center.xPos - self.__size.width / 2
        originYPos = 0
        if center.yPos >= 0:
            originYPos = center.yPos - self.__size.height / 2
        else:
            originYPos = center.yPos + self.__size.height / 2
        self.setOrigin(Point(originXPos, originYPos))
        
    def setX(self, xPos):
        self.__origin = Point(xPos, self.__origin.yPos)
        self.draw()
        
    def setY(self, yPos):
        self.__origin = Point(self.__origin.xPos, yPos)
        self.draw()
        
    def setWidth(self, width):
        self.__size = Size(width, self.__size.height)
        self.draw()
        
    def setHeight(self, height):
        self.__size = Size(self.__size.width, height)
        self.draw()
        
    def setCenterX(self, xPos):
        self.__origin = Point(xPos - self.__size.width / 2, self.__origin.yPos)
        self.draw()
        
    def setCenterY(self, yPos):
        self.__origin = Point(self.__origin.xPos, yPos - self.__size.height / 2)
        self.draw()
        
    def setFillColor(self, fillColor):
        self.__fillColor = fillColor
        self.draw()
        
    def setBorderColor(self, borderColor):
        self.__borderColor = borderColor
        self.draw()
        
    def resetShape(self, origin, size):
        self.setSize(self, size)
        self.setOrigin(self, origin)
        self.setCenter(self, Point(origin.xPos + size.width / 2, origin.yPos + size.height / 2))
        
    #Setup non animated turtle
    @staticmethod
    def setup_turtle(self, canvas, t):
        t.speed(0)
        t.hideturtle()
        t.penup()
        return t
        
    #Use these to set the values in the setters
    @abc.abstractmethod
    def draw(self):
        return