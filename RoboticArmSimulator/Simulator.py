import turtle
from RoboticArmSimulator.Circle import Circle
from RoboticArmSimulator.Rectangle import Rectangle
from RoboticArmSimulator.Point import Point
from RoboticArmSimulator.Size import Size


class Simulator:
    
    """
    Instance variables:
    
    Joints:
    wrist - Contains information about the wrist joint
    elbow - Contains information about the elbow joint
    shoulder - Contains information about the shoulder joint
    
    Limbs:
    forearm - Contains information about the forearm
    arm - Contains information about the arm
    hand - Contains information about the hand
    
    Class variables:
    screenLock - Prevents stack overflow from occurring due to too many mouse_dragged calls
    """
    screenLock = 1
    
    def __init__(self, canvas):
        
        # Main turtle
        t = Simulator.setup_turtle(canvas)
        t.pencolor("#000000")
        
        width = float(canvas['width'])
        height = float(canvas['height'])
        
        # Drawing coordinates, uncomment to use
        # Simulator.drawPlane(self, width, height, t)
        
        # Draw hand rect
        pvc_width = (1 / 12) * width
        self.hand = Rectangle(Point((1.375 / 30) * width, height / 2 - pvc_width / 2),
                              Size((1 / 6) * width, pvc_width), canvas, 'gray')

        # Draw forearm rect
        self.forearm = Rectangle(Point((6.375 / 30) * width, height / 2 - pvc_width / 2),
                                 Size((1 / 3) * width, pvc_width), canvas, 'gray')

        # Draw arm rect
        self.arm = Rectangle(Point((16.375 / 30) * width, 100),
                             Size((1 / 3) * width, pvc_width), canvas, 'gray')
        
        # Draw wrist joint
        wrist_radius = (1 / 20) * width
        self.wrist = Circle(Point((4.875 / 30) * width, height / 2 - wrist_radius), wrist_radius, canvas, 'red')
        
        # Draw elbow joint
        elbow_radius = (2.25 / 30) * width
        self.elbow = Circle(Point((14.125 / 30) * width, height / 2 - elbow_radius), elbow_radius, canvas, 'red')
        
        # Draw shoulder joint
        shoulder_radius = (2.25 / 30) * width
        self.shoulder = Circle(Point((24.125 / 30) * width, height / 2 - shoulder_radius), shoulder_radius,
                               canvas, 'red')

        # Mouse click/dragged detection
        canvas.bind("<Button-1>", self.mouse_clicked)
        canvas.bind("<B1-Motion>", self.mouse_dragged)
        
    # Used to find the middle of the screen
    @staticmethod
    def draw_plane(width, height, t):
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
        
    # Setup non animated turtle
    @staticmethod
    def setup_turtle(canvas):
        t = turtle.RawTurtle(canvas)
        t.speed(0)
        t.hideturtle()
        t.penup()
        return t
        
    # Mouse click event
    def mouse_clicked(self, event):
        print("Clicked at", event.x, event.y)
        print("Origin at", self.arm.getx(), self.arm.gety())
        print("Size of", self.arm.get_width(), self.arm.get_height())
        print("\n")
        if self.arm.contains(event):
            print('contains')
        
    # Mouse dragged event
    def mouse_dragged(self, event):
        if Simulator.screenLock == 1:
            Simulator.screenLock = 0
            print("Dragged to", event.x, event.y)
            Simulator.screenLock = 1
