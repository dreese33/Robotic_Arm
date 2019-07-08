from RoboticArmSimulator.Shape import Shape


class Rectangle(Shape):
    
    def __init__(self, origin, size, masterCanvas, fillColor = None, borderColor = None):
        super(Rectangle, self).__init__(origin, size, masterCanvas, fillColor, borderColor)
        self.setOrigin(origin)
        
    def draw(self, origin = None, size = None, fillColor = None, borderColor = None):
        t = self.getTurtle()
        #t.clear()
        t.clear()
        t.penup()
        
        if origin == None:
            origin = self.getOrigin()
            
        if size == None:
            size = self.getSize()
            
        if fillColor == None:
            fillColor = self.getFillColor()
        
        t.setx(self.getSize().width / 2)
        t.sety(self.getSize().height / 2)
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
        
    def drawTestShape(self, origin = None, size = None, fillColor = None, borderColor = None):
        t = self.getTest()
        t.clear()
        t.penup()
        
        origin = self.getOriginCartesian()
            
        if size == None:
            size = self.getSize()
            
        if fillColor == None:
            fillColor = self.getFillColor()
        
        t.setx(origin.xPos)
        t.sety(origin.yPos + self.getMasterCanvasSize().height / 2 - self.getSize().height / 2)
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
