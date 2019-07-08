from tkinter import *
import turtle
from RoboticArmSimulator.Point import Point
from RoboticArmSimulator.Size import Size
import abc


# Requires modification for setter methods to work
# Based on computer coordinate system primarily (the one used in tkinters Canvas)
# Also contains conversion to cartesian coordinate system (the one used by turtle)
class Shape(object):
    
    """
    __cartesianOrigin - Initial point of shape, stored in cartesian coordinate system
    __computerOrigin - Initial point of shape, stored in computer coordinate system
    __size - Width and height of shape (width, height)
    __canvas - Canvas shape is being drawn on
    __masterCanvas - Canvas holding the primary canvas
    __turtle - Turtle drawing the shape
    __canvasSize - Size of the canvas
    __masterCanvasSize - Dimension of the master canvas
    __fillColor - Color to fill Shape with, no fill if None
    __borderColor - Color for border of shape
    __test - TEST
    """
    
    def __init__(self, origin, size, masterCanvas, fillColor = None, borderColor = None):
        self.__masterCanvas = masterCanvas
        self.__canvas = Canvas(master = masterCanvas, width = size.width, height = size.height, bd = 0, highlightthickness = 0)
        self.__canvasSize = Size(int(self.__canvas['width']), int(self.__canvas['height']))
        
        self.__size = size
        self.__computerOrigin = origin
        
        if origin.yPos == 0:
            self.__cartesianOrigin = Point(origin.xPos - self.__canvasSize.width / 2, origin.yPos - self.__canvasSize.height / 2)
        else:
            self.__cartesianOrigin = Point(origin.xPos - self.__canvasSize.width / 2, self.__canvasSize.height / 2 - origin.yPos)
        
        self.__masterCanvasSize = Size(int(masterCanvas['width']), int(masterCanvas['height']))
        self.__canvas.place(relx = origin.xPos / self.__masterCanvasSize.width, rely = origin.yPos / self.__masterCanvasSize.height)
        
        self.__fillColor = fillColor
        self.__borderColor = borderColor
        
        #Setup turtle
        self.__turtle = Shape.setup_turtle(self, self.__canvas)
        self.draw()
        
        self.__test = Shape.setup_turtle(self, self.__masterCanvas)
        self.__test._tracer(0)
        #self.drawTestShape()
      
    #Getters
    def getTest(self):
        return self.__test
    
    def getMasterCanvasSize(self):
        return self.__masterCanvasSize
    
    def getMasterCanvas(self):
        return self.__masterCanvas
        
    def getCanvasSize(self):
        return self.__canvasSize
    
    def getCenter(self):
        return Point(self.__size.width / 2 + self.__computerOrigin.xPos, self.__size.height / 2 + self.__computerOrigin.yPos)
    
    def getCenterCartesian(self):
        return Point(self.__size.width / 2 + self.__certesianOrigin.xPos, self.__size.height / 2 + self.__cartesianOrigin.yPos)
    
    def getSize(self):
        return self.__size
    
    def getOrigin(self):
        return self.__computerOrigin
    
    def getOriginCartesian(self):
        return self.__cartesianOrigin
    
    def getParent(self):
        return self.__canvas
    
    def getTurtle(self):
        return self.__turtle
    
    def getFillColor(self):
        return self.__fillColor
    
    def getBorderColor(self):
        return self.__borderColor
    
    #Setters
    def setSize(self, size):
        self.__size = size
        self.draw()
        
    def setOriginTest(self, origin):
        self.__computerOrigin = origin
        if origin.yPos == 0:
            self.__cartesianOrigin = Point(origin.xPos - self.__canvasSize.width / 2, origin.yPos - self.__canvasSize.height / 2)
        else:
            self.__cartesianOrigin = Point(origin.xPos - self.__canvasSize.width / 2, self.__canvasSize.height / 2 - origin.yPos)
        self.drawTestShape()
        
    #Tested
    def setOrigin(self, origin):
        self.__computerOrigin = origin
        if origin.yPos == 0:
            self.__cartesianOrigin = Point(origin.xPos - self.__canvasSize.width / 2, origin.yPos - self.__canvasSize.height / 2)
        else:
            self.__cartesianOrigin = Point(origin.xPos - self.__canvasSize.width / 2, self.__canvasSize.height / 2 - origin.yPos)
        self.__canvas.place(relx = origin.xPos / self.__masterCanvasSize.width, rely = origin.yPos / self.__masterCanvasSize.height)
        
    #Tested
    def setCenter(self, center):
        originXPos = center.xPos - self.__size.width / 2
        originYPos = 0
        if center.yPos >= 0:
            originYPos = center.yPos - self.__size.height / 2
        else:
            originYPos = center.yPos + self.__size.height / 2
        self.setOrigin(Point(originXPos, originYPos))
        
    #Tested
    def setX(self, xPos):
        self.__cartesianOrigin = Point(xPos - self.__canvasSize.width / 2, self.__cartesianOrigin.yPos)
        self.__computerOrigin = Point(xPos, self.__computerOrigin.yPos)
        self.__canvas.place(relx = self.__computerOrigin.xPos / self.__masterCanvasSize.width, rely = self.__computerOrigin.yPos / self.__masterCanvasSize.height)
        
    #Tested
    def setY(self, yPos):
        self.__computerOrigin = Point(self.__computerOrigin.xPos, yPos)
        if yPos == 0:
            self.__cartesianOrigin = Point(self.__cartesianOrigin.xPos, yPos - self.__canvasSize.height / 2)
        else:
            self.__cartesianOrigin = Point(self.__cartesianOrigin.xPos, self.__canvasSize.height / 2 - yPos)
        self.__canvas.place(relx = self.__computerOrigin.xPos / self.__masterCanvasSize.width, rely = self.__computerOrigin.yPos / self.__masterCanvasSize.height)
        
    def setWidth(self, width):
        self.__size = Size(width, self.__size.height)
        self.draw()
        
    def setHeight(self, height):
        self.__size = Size(self.__size.width, height)
        self.draw()
        
    #Tested
    def setCenterX(self, xPos):
        self.__computerOrigin = Point(xPos - self.__size.width / 2, self.__computerOrigin.yPos)
        self.__cartesianOrigin = Point(xPos - self.__size.width / 2, self.__cartesianOrigin.yPos)
        self.__canvas.place(relx = self.__computerOrigin.xPos / self.__masterCanvasSize.width, rely = self.__computerOrigin.yPos / self.__masterCanvasSize.height)
        
    #Tested
    def setCenterY(self, yPos):
        originYPos = 0
        if yPos >= 0:
            originYPos = yPos - self.__size.height / 2
        else:
            originYPos = yPos + self.__size.height / 2
        
        computerOrigin = Point(self.__computerOrigin.xPos, originYPos)
        self.setOrigin(computerOrigin)
        
    def setFillColor(self, fillColor):
        self.__fillColor = fillColor
        self.draw()
        
    def setBorderColor(self, borderColor):
        self.__borderColor = borderColor
        self.draw()
        
    def resetShape(self, origin, size):
        self.setSize(self, size)
        self.setOrigin(self, origin)
        
    #Setup non animated turtle
    @staticmethod
    def setup_turtle(self, canvas):
        #t = turtle.RawTurtle(canvas)
        t = turtle.Pen()
        t.speed(0)
        t.hideturtle()
        t.penup()
        return t
        
    #Use these to set the values in the setters
    @abc.abstractmethod
    def draw(self):
        return
    
    @abc.abstractmethod
    def drawTestShape(self):
        return