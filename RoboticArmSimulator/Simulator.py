import turtle

class Simulator():
    
    def __init__(self, canvas):
        t = turtle.RawTurtle(canvas)
        t.speed(0)
        t.hideturtle()
        t.pencolor("#000000")
        
        width = int(canvas['width'])
        height = int(canvas['height'])
        
        #Drawing coordinates, uncomment to use
        #Simulator.drawPlane(self, width, height, t)
        
        #Draw wrist rect
        t.penup()
        t.fillcolor("gray")
        t.setx(((3.875 / 30) * width) - (width / 2))
        t.sety(-(1 / 24) * width)
        
        pvc_width = (1 / 12) * width
        t.begin_fill()
        Simulator.drawRectangle(self, pvc_width, pvc_width * 2, t)
        t.end_fill()
        
        #Draw elbow rect
        t.setx(((11.375 / 30) * width) - (width / 2))
        elbow_width = (1 / 3) * width
        t.begin_fill()
        Simulator.drawRectangle(self, pvc_width, elbow_width, t)
        t.end_fill()
        
        #Draw shoulder rect
        t.setx(((21.375 / 30) * width) - (width / 2))
        shoulder_width = (1 / 3) * width
        t.begin_fill()
        Simulator.drawRectangle(self, pvc_width, shoulder_width, t)
        t.end_fill()
        
        #Set fill
        t.fillcolor("red")
        
        #Draw wrist joint
        wrist_radius = (1 / 20) * width
        t.setx(((6.375 / 30) * width) - (width / 2))
        t.sety(-wrist_radius)
        t.pendown()
        t.begin_fill()
        t.circle(wrist_radius)
        t.end_fill()
        t.penup()
        
        #Draw elbow joint
        elbow_radius = (2.25 / 30) * width
        t.setx(((16.375 / 30) * width) - (width / 2))
        t.sety(-elbow_radius)
        t.pendown()
        t.begin_fill()
        t.circle(elbow_radius)
        t.end_fill()
        t.penup()
        
        #Draw shoulder joint
        shoulder_radius = (2.25 / 30) * width
        t.setx(((26.375 / 30) * width) - (width / 2))
        t.sety(-shoulder_radius)
        t.pendown()
        t.begin_fill()
        t.circle(shoulder_radius)
        t.end_fill()
        t.penup()
        
    #Used to find the middle of the screen
    @staticmethod
    def drawPlane(self, width, height, t):
        t.penup()
        t.setx(-width / 2)
        t.sety(0)
        t.pendown()
        t.forward(width)
        t.penup()
        t.setx(0)
        t.sety(-height / 2)
        t.left(90)
        t.pendown()
        t.forward(height)
        t.right(90)
        t.penup()
        
    #Starting point is the middle of the bottom of the rectangle
    @staticmethod
    def drawRectangle(self, width, armlength, t):
        t.pendown()
        t.forward(armlength / 2)
        t.left(90)
        t.forward(width)
        t.left(90)
        t.forward(armlength)
        t.left(90)
        t.forward(width)
        t.left(90)
        t.forward(armlength / 2)
        t.penup()