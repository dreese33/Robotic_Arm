import math
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("TkAgg")
LARGE_FONT = ("Verdana", 12)

"""
class Simulator(tk.Tk):
    
    com
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
    com
    screenLock = 1
    rotating = False

    def init(self):
        pass

    def __init__(self):

        GraphSimulator()

    com
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


class Simulator:

    """
    Class Variables:

    left_pressed - Left mouse button is pressed
    running - Determines whether or not to start a new Simulator
    simulator_plot_width - The width of the Simulator pyplot axis

    Instance Variables:

    Joints:
    wrist - Wrist of the arm
    elbow - Elbow of the arm
    shoulder - Rotating base portion of the arm, the shoulder

    Limbs:
    hand - Grabber portion of the arm
    forearm - Middle portion of the arm. Attaches wrist to elbow.
    arm - Last segment of the arm. Attaches elbow to shoulder.
    """

    left_pressed = False
    running = False
    simulator_plot_width = 1000

    def __init__(self):

        if not Simulator.running:
            Simulator.running = True

            quadrant_width = Simulator.simulator_plot_width / 2

            figure = plt.figure(num='Robotic Arm Simulator', figsize=(5, 5))
            figure.canvas.mpl_connect('button_press_event', self.mouse_clicked)
            figure.canvas.mpl_connect('button_release_event', Simulator.mouse_released)
            figure.canvas.mpl_connect('close_event', Simulator.handle_close)

            plt.title('Simulator')

            # Shapes
            wrist_radius = (1 / 20) * Simulator.simulator_plot_width
            elbow_radius = (4.5 / 60) * Simulator.simulator_plot_width     # Same as shoulder radius
            pvc_height = (2.5 / 30) * Simulator.simulator_plot_width

            hand_width = (1 / 6) * Simulator.simulator_plot_width
            forearm_width = (1 / 3) * Simulator.simulator_plot_width       # Same as arm width

            self.wrist = plt.Circle((0, 0), radius=wrist_radius, fc='r')
            plt.gca().add_patch(self.wrist)

            self.elbow = plt.Circle((200, 10), radius=elbow_radius, fc='r')
            plt.gca().add_patch(self.elbow)

            self.shoulder = plt.Circle((-100, -200), radius=elbow_radius, fc='r')
            plt.gca().add_patch(self.shoulder)

            self.hand = plt.Rectangle((0, 200), height=pvc_height, width=hand_width, fc='gray')
            plt.gca().add_patch(self.hand)

            self.forearm = plt.Rectangle((100, 300), height=pvc_height, width=forearm_width, fc='gray')
            plt.gca().add_patch(self.forearm)

            self.arm = plt.Rectangle((100, 400), height=pvc_height, width=forearm_width, fc='gray')
            plt.gca().add_patch(self.arm)

            plt.axis([-quadrant_width, quadrant_width, -quadrant_width, quadrant_width])

            plt.show()

    def mouse_clicked(self, event):
        Simulator.left_pressed = True
        print("You pressed: ", event.x, event.y)
        self.wrist.center = Simulator.rotate((100, 0), self.wrist.get_center(), 0.1)
        plt.gca().figure.canvas.draw()

    @staticmethod
    def mouse_released(event):
        Simulator.left_pressed = False
        print("Released at: ", event.x, event.y)

    @staticmethod
    def handle_close(event):
        Simulator.running = False
        print("Closing")


    # https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
    # Credit for this function to Mark Dickinson
    @staticmethod
    def rotate(origin, point, angle):
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy
