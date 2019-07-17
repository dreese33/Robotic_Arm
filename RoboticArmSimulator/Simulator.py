import turtle
import math
import tkinter as tk
import ctypes

import matplotlib.pyplot as plt
import matplotlib
from matplotlib import animation

matplotlib.use("TkAgg")
LARGE_FONT = ("Verdana", 12)


class Simulator(tk.Tk):
    
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
    rotating = False
    interfile_master_canvas_size = (0, 0)

    def init(self):
        pass

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #tk.Tk.wm_title(self, "Sea of BTC client")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = PageThree()

        self.frames[PageThree] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        #frame.canvas.mpl_connect('button_press_event', self.mouse_clicked)

        self.show_frame(PageThree)
        frame.canvas.get_tk_widget().focus_force()
        print("Working")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def mouse_clicked(self, event):
        print("You pressed: ", event.x, event.y)
    """
    def __init__(self, canvas):
        
        # Main turtle
        #t = Simulator.setup_turtle(canvas)
        #t.pencolor("#000000")
        
        width = int(canvas['width'])
        height = int(canvas['height'])
        
        # Drawing coordinates, uncomment to use
        # Simulator.draw_plane(width, height, t)
        #canvas.create_rectangle(30, 10, 120, 80,
        #    outline="#fb0", fill="#ab1")
        #self.canvas = canvas
        #self.oval = canvas.create_oval(10, 10, 80, 80, outline="#f11", fill="#1f1", width=2)


        
        # Draw hand rect
        pvc_width = (1 / 12) * width
        self.hand = Rectangle(Point((1.375 / 30) * width, height / 2 - pvc_width / 2),
                              Size((1 / 6) * width, pvc_width), canvas, 'gray')

        # Draw forearm rect
        self.forearm = Rectangle(Point((6.375 / 30) * width, height / 2 - pvc_width / 2),
                                 Size((1 / 3) * width, pvc_width), canvas, 'gray')

        # Draw arm rect
        self.arm = Rectangle(Point((16.375 / 30) * width, height / 2 - pvc_width / 2),
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
        canvas.bind("<B1-Motion>", self.mouse_dragged)"""

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
        t._tracer(0)
        t.speed(0)
        t.hideturtle()
        t.penup()
        return t

    """
    # Mouse click event
    def mouse_clicked(self, event):
        #print("Clicked at", event.x, event.y)
        #print("Origin at", self.arm.getx(), self.arm.gety())
        #print("Center at", self.arm.get_center().x, self.arm.get_center().y)
        #print("Size of", self.arm.get_width(), self.arm.get_height())
        print("Clicked: ", event.x, event.y)
        print("\n")
        #self.arm.rotate_center(10)"""
        
    # Mouse dragged event
    def mouse_dragged(self, event):
        if Simulator.screenLock == 1:
            Simulator.screenLock = 0
            print("\n")
            #print("Dragged to", event.x, event.y)
            #self.arm.rotate_center(10)
            #self.canvas.move(self.oval, event.x, event.y)
            Simulator.screenLock = 1


class PageThree:

    def __init__(self):
        plt.figure(num='Robotic Arm Simulator', figsize=(5, 5)).canvas.mpl_connect('button_press_event', self.mouse_clicked)
        plt.title('Simulator')

        # Shapes
        self.circle = plt.Circle((100, 100), radius=150, fc='r')
        plt.gca().add_patch(self.circle)

        circle1 = plt.Circle((0, 0), radius=100, fc='r')
        plt.gca().add_patch(circle1)

        circle2 = plt.Circle((-100, -200), radius=100, fc='r')
        plt.gca().add_patch(circle2)

        plt.axis([-500, 500, -500, 500])

        plt.show()

    def mouse_clicked(self, event):
        print("You pressed: ", event.x, event.y)
        self.circle.center = PageThree.rotate((0, 0), self.circle.get_center(), 0.1)
        plt.gca().figure.canvas.draw()


    # https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
    # Credit for this function to Mark Dickinson
    @staticmethod
    def rotate(origin, point, angle):
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy
