from tkinter import *
from RoboticArmSimulator.Point import Point
from RoboticArmSimulator.Size import Size
import abc

#Requires modification for setter methods to work
class Shape(object):
    
    """
    __origin - Initial point of shape
    __size - Width and height of shape (width, height)
    __center - Center point of the shape
    __canvas - Canvas shape is being drawn on
    __turtle - Turtle drawing the shape
    __canvasSize - Size of the canvas
    """
    
    def __init__(self, origin, size, canvas, t):
        self.__origin = origin
        self.__size = size
        self.__center = Point(size.width / 2 + origin.xPos, size.height / 2 + origin.yPos)
        self.__canvas = canvas
        self.__turtle = t
        self.__canvasSize = Size(int(canvas['width']), int(canvas['height']))
        
        #Setup turtle
        Shape.setup_turtle(self, canvas, t)
      
    #Getters
    def getCanvasSize(self):
        return self.__canvasSize
    
    def getCenter(self):
        return self.__center
    
    def getSize(self):
        return self.__size
    
    def getOrigin(self):
        return self.__origin
    
    def getParent(self):
        return self.__canvas
    
    def getTurtle(self):
        return self.__turtle
    
    #Setters
    def setSize(self, size):
        self.__size = size
        
    def setOrigin(self, origin):
        self.__origin = origin
        
    def setCenter(self, center):
        self.__center = center
        
    def setX(self, xPos):
        self.__origin = Point(xPos, self.__origin.y)
        
    def setY(self, yPos):
        self.__origin = Point(self.__origin.x, yPos)
        
    def setWidth(self, width):
        self.__size = Size(width, self.__size.height)
        
    def setHeight(self, height):
        self.__size = Size(self.__size.width, height)
        
    def setCenterX(self, xPos):
        self.__center = Point(xPos, self.__center.y)
        
    def setCenterY(self, yPos):
        self.__center = Point(self.__center.x, yPos)
        
    def resetShape(self, origin, size):
        setSize(self, size)
        setOrigin(self, origin)
        setCenter(self, Point(origin.xPos + size.width / 2, origin.yPos + size.height / 2))
        
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
    
    @abc.abstractmethod
    def drawFill(self):
        return