import turtle
from tkinter import *
from RoboticArmSimulator.Circle import Circle
from RoboticArmSimulator.Rectangle import Rectangle
from RoboticArmSimulator.Point import Point
from RoboticArmSimulator.Size import Size

class Simulator():
    
    """
    Instance variables:
    width - width of canvas
    height - height of canvas
    pvc_width - width of the pipe on the robot
    elbow_width - width of the elbow
    shoulder_width - width of shoulder
    wrist_radius - radius of the wrist joint
    elbot_radius - radius of the elbow joint
    shoulder_radius - radius of the shoulder joint
    
    Turtles:
    t - main turtle, Draws coordinate system if necessary
    wrist_turtle - Draws wrist joint
    elbow_turtle - Draws elbow joint
    shoulder_turtle - Draws shoulder joint
    
    Joints:
    wrist - Contains information about the wrist joint
    elbow - Contains information about the elbow joint
    shoulder - Contains information about the shoulder joint
    
    Limbs:
    forearm - Contains information about the forearm
    arm - Contains information about the arm
    hand - Contains information about the hand
    """
    
    def __init__(self, canvas):
        
        #Main turtle
        t = Simulator.setup_turtle(self, canvas)
        t.pencolor("#000000")
        
        width = int(canvas['width'])
        height = int(canvas['height'])
        
        #Drawing coordinates, uncomment to use
        #Simulator.drawPlane(self, width, height, t)
        
        #Draw hand rect
        wrist_turtle = Simulator.setup_turtle(self, canvas)
        pvc_width = (1 / 12) * width
        hand = Rectangle(Point((1.375 / 30) * width, height / 2 - pvc_width / 2), Size(pvc_width * 2, pvc_width), canvas, wrist_turtle, 'gray')
        
        #Draw forearm rect
        elbow_turtle = Simulator.setup_turtle(self, canvas)
        forearm = Rectangle(Point((6.375 / 30) * width, height / 2 - pvc_width / 2), Size((1 / 3) * width, pvc_width), canvas, elbow_turtle, 'gray')
        
        #Draw arm rect
        shoulder_turtle = Simulator.setup_turtle(self, canvas)
        arm = Rectangle(Point((16.375 / 30) * width, height / 2 - pvc_width / 2), Size((1 / 3) * width, pvc_width), canvas, shoulder_turtle, 'gray')
        
        #Draw wrist joint
        wrist_radius = (1 / 20) * width
        wrist = Circle(Point((6.375 / 30) * width, height / 2 - wrist_radius), wrist_radius, canvas, wrist_turtle, 'red')
        
        #Draw elbow joint
        elbow_radius = (2.25 / 30) * width
        elbow = Circle(Point((16.375 / 30) * width, height / 2 - elbow_radius), elbow_radius, canvas, elbow_turtle, 'red')
        
        #Draw shoulder joint
        shoulder_radius = (2.25 / 30) * width
        shoulder = Circle(Point((26.375 / 30) * width, height / 2 - shoulder_radius), shoulder_radius, canvas, shoulder_turtle, 'red')
        
        #Mouse click/dragged detection
        canvas.bind("<Button-1>", Simulator.mouse_clicked)
        canvas.bind("<B1-Motion>", Simulator.mouse_dragged)
        
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
        
    #Setup non animated turtle
    @staticmethod
    def setup_turtle(self, canvas):
        t = turtle.RawTurtle(canvas)
        t.speed(0)
        t.hideturtle()
        t.penup()
        return t
        
    #Mouse click event
    @staticmethod
    def mouse_clicked(event):
        print("Clicked at", event.x, event.y)
        
    #Mouse dragged event
    @staticmethod
    def mouse_dragged(event):
        print("Dragged to", event.x, event.y)