import math
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("TkAgg")
LARGE_FONT = ("Verdana", 12)


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
    forearm - Middle portion of the arm. Attaches wrist to elbow
    arm - Last segment of the arm. Attaches elbow to shoulder

    Limb Sizes:
    pvc_height - Height of all of the limbs
    hand_width - Width of the hand
    forearm_width - Width of the forearm and arm
    """

    left_pressed = False
    running = False
    simulator_plot_width = 1000
    arm_limbs = []
    arm_joints = []

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
            wrist_radius = (1 / 40) * Simulator.simulator_plot_width
            elbow_radius = (4.5 / 120) * Simulator.simulator_plot_width     # Same as shoulder radius

            self.pvc_height = (2.5 / 60) * Simulator.simulator_plot_width
            self.hand_width = (1 / 12) * Simulator.simulator_plot_width
            self.forearm_width = (1 / 6) * Simulator.simulator_plot_width       # Same as arm width

            wrist_center = (150, 100)
            elbow_center = (200, 10)
            shoulder_center = (-100, -200)

            # Limbs should be behind the joints
            self.hand = self._default_limb(self.hand_width)
            plt.gca().add_patch(self.hand)

            self.forearm = self._default_limb(self.forearm_width)
            plt.gca().add_patch(self.forearm)

            self.arm = self._default_limb(self.forearm_width)
            plt.gca().add_patch(self.arm)

            # Joints
            self.wrist = Simulator._add_joint(wrist_center, wrist_radius, 'r')
            plt.gca().add_patch(self.wrist)

            self.elbow = Simulator._add_joint(elbow_center, elbow_radius, 'r')
            plt.gca().add_patch(self.elbow)

            self.shoulder = Simulator._add_joint(shoulder_center, elbow_radius, 'r')
            plt.gca().add_patch(self.shoulder)

            self._update_limb_positions()

            plt.axis([-quadrant_width, quadrant_width, -quadrant_width, quadrant_width])

            plt.show()

    def _get_limb_origin(self, joint, limb_width):
        return joint.center[0] - limb_width, joint.center[1] - self.pvc_height / 2

    def _default_limb(self, width):
        return plt.Rectangle((0, 0), height=self.pvc_height, width=width, fc='gray')

    @staticmethod
    def _add_joint(center, radius, color_str):
        return plt.Circle(center, radius=radius, fc=color_str)

    def mouse_clicked(self, event):
        Simulator.left_pressed = True
        print("You pressed: ", event.x, event.y)
        self.wrist.center = Simulator.rotate((100, 0), self.wrist.get_center(), 0.1)
        self._update_limb_positions()

    def _update_limb_positions(self):
        self.hand.set_xy(self._get_limb_origin(self.wrist, self.hand_width))
        self.forearm.set_xy(self._get_limb_origin(self.elbow, self.forearm_width))
        self.arm.set_xy(self._get_limb_origin(self.shoulder, self.forearm_width))
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
