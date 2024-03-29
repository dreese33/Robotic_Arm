import math
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.transforms
from matplotlib.widgets import RadioButtons, Slider

matplotlib.use("TkAgg")
LARGE_FONT = ("Verdana", 12)


class Simulator:

    """
    Class Variables:

    left_pressed - Left mouse button is pressed
    running - Determines whether or not to start a new Simulator
    simulator_plot_width - The width of the Simulator pyplot axis
    arm_limbs - Limbs listed in order
    arm_joints - Joints listed in order
    total_rotations - Array listing the total amount each joint should be rotated
    firsts - Array containing values regarding the first movement of each joint

    Instance Variables:

    current_fig_axes - The axes of the current figure
    cw - 0 means clockwise, 1 means counterclockwise
    previous_arrow - 0 previous movement was not made by an arrow, 1 right, 2 left, 3 up, 4 down
    degree_quadrants - Quadrants to determine arrow movement of simulator

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

    Radio Buttons:
    joint_selector - Select which joint to use
    clockwise_selector - Select clockwise or counterclockwise
    """

    left_pressed = False
    running = False
    simulator_plot_width = 1000

    arm_limbs = []
    arm_joints = []
    motors = []

    total_rotations = [0, 0, 0]
    unlocked = True

    firsts = [True, True, True]
    simulator_lock = True

    def __init__(self, motors):

        if not Simulator.running:
            Simulator.running = True
            Simulator.motors = motors

            quadrant_width = Simulator.simulator_plot_width / 2

            figure = plt.figure(num='Robotic Arm Simulator', figsize=(7, 6))
            figure.canvas.mpl_connect('button_press_event', self.mouse_clicked)
            figure.canvas.mpl_connect('button_release_event', self.mouse_released)
            figure.canvas.mpl_connect('close_event', Simulator.handle_close)
            figure.canvas.mpl_connect('motion_notify_event', self.mouse_dragged)
            #figure.canvas.mpl_connect('key_press_event', self.radio_control)
            figure.canvas.mpl_connect('key_press_event', self.arrow_key_listener)

            plt.axis([-quadrant_width, quadrant_width, -quadrant_width, quadrant_width])
            plt.title('Simulator')
            plt.subplots_adjust(left=0.4, bottom=0.3)
            self.current_fig_axes = plt.gca()

            # Shapes
            wrist_radius = (1 / 40) * Simulator.simulator_plot_width
            elbow_radius = (4.5 / 120) * Simulator.simulator_plot_width     # Same as shoulder radius

            self.pvc_height = (2.5 / 60) * Simulator.simulator_plot_width
            self.hand_width = (1 / 12) * Simulator.simulator_plot_width
            self.forearm_width = (1 / 6) * Simulator.simulator_plot_width       # Same as arm width

            shoulder_center = (0, 0)
            elbow_center = (shoulder_center[0] - self.forearm_width, 0)
            wrist_center = (elbow_center[0] - self.forearm_width, 0)

            # Key control variables
            self.arrow_key_pressed = False

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
            self.curr_joint_rotation = 0
            self.cw = 0
            self.previous_arrow = 0

            self.degree_quadrants = [Simulator.to_radians(90),
                                     Simulator.to_radians(180),
                                     Simulator.to_radians(270),
                                     Simulator.to_radians(360)]

            # List the joints and limbs in order
            Simulator.arm_joints = [self.wrist, self.elbow, self.shoulder]
            Simulator.arm_limbs = [self.hand, self.forearm, self.arm]

            axcolor = 'lightgoldenrodyellow'
            rax = plt.axes([0.05, 0.6, 0.17, 0.20], facecolor=axcolor)

            # Select joint
            self.joint_selector = RadioButtons(rax, ('wrist', 'elbow', 'shoulder'))
            self.joint_selector.on_clicked(self.set_rotation_point)

            rax = plt.axes([0.05, 0.4, 0.15, 0.15], facecolor=axcolor)

            self.clockwise_selector = RadioButtons(rax, ('CW', 'CCW'))
            self.clockwise_selector.on_clicked(self.set_clockwise)

            rax = plt.axes([0.40, 0.17, 0.50, 0.03])

            init_val = 16
            self.speed = Simulator.to_radians(init_val)

            self.speed_slider = Slider(rax, 'Speed' + '\n' + '(in degrees)', 0.1, 20, valinit=init_val)
            self.speed_slider.on_changed(self.update_speed)

            # Text
            axbox_wrist_text = plt.axes([0.31, 0.07, 0.1, 0.05])
            axbox_wrist_text.text(0, 0, 'Wrist: ', fontsize=12)
            axbox_wrist_text.axis('off')

            axbox_elbow_text = plt.axes([0.51, 0.07, 0.1, 0.05])
            axbox_elbow_text.text(0, 0, 'Elbow: ', fontsize=12)
            axbox_elbow_text.axis('off')

            axbox_shoulder_text = plt.axes([0.71, 0.07, 0.1, 0.05])
            axbox_shoulder_text.text(0, 0, 'Shoulder: ', fontsize=12)
            axbox_shoulder_text.axis('off')

            initial_text = r'${:.0f}\degree$'.format(0)
            self.axbox_wrist = plt.axes([0.40, 0.07, 0.1, 0.05])
            self.axbox_wrist.text(0, 0, initial_text, fontsize=15)
            self.axbox_wrist.axis('off')

            self.axbox_elbow = plt.axes([0.61, 0.07, 0.1, 0.05])
            self.axbox_elbow.text(0, 0, initial_text, fontsize=15)
            self.axbox_elbow.axis('off')

            self.axbox_shoulder = plt.axes([0.84, 0.07, 0.1, 0.05])
            self.axbox_shoulder.text(0, 0, initial_text, fontsize=15)
            self.axbox_shoulder.axis('off')
            
            self.axboxes = [self.axbox_wrist, self.axbox_elbow, self.axbox_shoulder]

            plt.axes(self.current_fig_axes)

            plt.show()

    def set_rotation_point(self, label):
        if label == 'wrist':
            self.curr_joint_rotation = 0
        elif label == 'elbow':
            self.curr_joint_rotation = 1
        else:
            self.curr_joint_rotation = 2

    def set_clockwise(self, label):
        if label == 'CW':
            self.cw = 0
        else:
            self.cw = 1

    def update_speed(self, speed):
        self.speed = Simulator.to_radians(speed)

    def _get_limb_origin(self, joint, limb_width):
        return joint.center[0] - limb_width, joint.center[1] - self.pvc_height / 2

    def _default_limb(self, width):
        return plt.Rectangle((0, 0), height=self.pvc_height, width=width, fc='gray')

    @staticmethod
    def _add_joint(center, radius, color_str):
        return plt.Circle(center, radius=radius, fc=color_str)

    def _update_angles1(self, degrees):
        for val in range(len(degrees)):
            self.axboxes[val].clear()
            self.axboxes[val].text(0, 0, r'${:.0f}\degree$'.format(Simulator.to_degrees(degrees[val])), fontsize=15)
            self.axboxes[val].axis('off')

    def _update_angles(self, degrees):
        if self.curr_joint_rotation == 0:
            self.axbox_wrist.clear()
            self.axbox_wrist.text(0, 0, r'${:.0f}\degree$'.format(degrees), fontsize=15,
                                  bbox=dict(facecolor='none', edgecolor='black'))
            self.axbox_wrist.axis('off')
        elif self.curr_joint_rotation == 1:
            self.axbox_elbow.clear()
            self.axbox_elbow.text(0, 0, r'${:.0f}\degree$'.format(degrees), fontsize=15,
                                  bbox=dict(facecolor='none', edgecolor='black'))
            self.axbox_elbow.axis('off')
        elif self.curr_joint_rotation == 2:
            self.axbox_shoulder.clear()
            self.axbox_shoulder.text(0, 0, r'${:.0f}\degree$'.format(degrees), fontsize=15,
                                     bbox=dict(facecolor='none', edgecolor='black'))
            self.axbox_shoulder.axis('off')
        else:
            print("Something went wrong in _update_angles")

    def _update_limb_positions(self):
        self.hand.set_xy(self._get_limb_origin(self.wrist, self.hand_width))
        self.forearm.set_xy(self._get_limb_origin(self.elbow, self.forearm_width))
        self.arm.set_xy(self._get_limb_origin(self.shoulder, self.forearm_width))
        #plt.gca().figure.canvas.draw()

    def rotate_joints(self, radians):

        base = Simulator.arm_joints[self.curr_joint_rotation]

        if self.cw == 0:
            radians = -radians

        # Handle joints first
        for i in range(self.curr_joint_rotation + 1):
            if i != 0:
                joint = Simulator.arm_joints[i - 1]
                joint.center = Simulator.rotate(base.center, joint.center, radians)

        for i in range(self.curr_joint_rotation + 1):

            Simulator.total_rotations[i] += radians

            t = matplotlib.transforms.Affine2D().rotate_around(Simulator.arm_joints[i].center[0],
                                                               Simulator.arm_joints[i].center[1],
                                                               Simulator.total_rotations[i])
            t += plt.gca().transData
            Simulator.arm_limbs[i].set_transform(t)

        self._update_limb_positions()

        for i in range(len(Simulator.total_rotations)):
            Simulator.total_rotations[i] = self.simplify_radians(Simulator.total_rotations[i])
            
        #print("About to update angles")
        self._update_angles1(Simulator.total_rotations)
        Simulator.motors[self.curr_joint_rotation].step_motor_degrees(Simulator.to_degrees(radians))
        #self._update_angles(Simulator.to_degrees(Simulator.total_rotations[self.curr_joint_rotation]))
        plt.gca().figure.canvas.draw()

    @staticmethod
    def get_empty_transform():
        return matplotlib.transforms.Affine2D().rotate_around(0, 0, 0)

    def mouse_clicked(self, event):
        if event.inaxes == self.current_fig_axes:
            Simulator.left_pressed = True
            print("You pressed: ", event.x, event.y)
            self.rotate_joints(self.speed)
            self.previous_arrow = 0

    def mouse_released(self, event):
        if event.inaxes == self.current_fig_axes:
            Simulator.left_pressed = False
            print("Released at: ", event.x, event.y)

    def mouse_dragged(self, event):
        if Simulator.left_pressed:
            if Simulator.unlocked:
                Simulator.unlocked = False
                self.previous_arrow = 0
                self.rotate_joints(self.speed)
                Simulator.unlocked = True

    @staticmethod
    def to_radians(degrees):
        return degrees * (math.pi / 180)

    @staticmethod
    def to_degrees(radians):
        return radians * (180 / math.pi)

    @staticmethod
    def simplify_radians(radians):
        while radians < 0:
            radians += 6.28

        while radians > 6.28:
            radians -= 6.28

        return radians

    def reverse_clockwise(self):
        if self.cw == 0:
            self.cw = 1
            self.clockwise_selector.set_active(1)
        else:
            self.cw = 0
            self.clockwise_selector.set_active(0)

    def opposite_arrow_pressed(self, current_arrow):
        self.reverse_clockwise()
        self.rotate_joints(self.speed)
        self.previous_arrow = current_arrow

    # Adds key controls to the radio buttons for optimal control of the simulator
    #def radio_control(self, event):
        

    # Move the robot based on its current joint position and arrow keys
    def arrow_key_listener(self, event):
        if Simulator.simulator_lock:
            Simulator.simulator_lock = False
            if event.key == 'c':
                self.previous_arrow = 0
                self.reverse_clockwise()
            elif event.key == '1':
                self.curr_joint_rotation = 0
                self.joint_selector.set_active(0)
                self.previous_arrow = 0
            elif event.key == '2':
                self.curr_joint_rotation = 1
                self.joint_selector.set_active(1)
                self.previous_arrow = 0
            elif event.key == '3':
                self.curr_joint_rotation = 2
                self.joint_selector.set_active(2)
                self.previous_arrow = 0
            elif event.key == 'right':
                if self.previous_arrow == 2:
                    self.opposite_arrow_pressed(1)
                else:
                    if self.previous_arrow != 1:
                        self.move_robot_right()
                        self.previous_arrow = 1
                    else:
                        self.rotate_joints(self.speed)
            elif event.key == 'left':
                if self.previous_arrow == 1:
                    self.opposite_arrow_pressed(2)
                else:
                    if self.previous_arrow != 2:
                        self.move_robot_left()
                        self.previous_arrow = 2
                    else:
                        self.rotate_joints(self.speed)
            elif event.key == 'up':
                if self.previous_arrow == 4:
                    self.opposite_arrow_pressed(3)
                else:
                    if self.previous_arrow != 3:
                        self.move_robot_up()
                        self.previous_arrow = 3
                    else:
                        self.rotate_joints(self.speed)
            elif event.key == 'down':
                if self.previous_arrow == 3:
                    self.opposite_arrow_pressed(4)
                else:
                    if self.previous_arrow != 4:
                        self.move_robot_down()
                        self.previous_arrow = 4
                    else:
                        self.rotate_joints(self.speed)
            #print("Set to true")
            Simulator.simulator_lock = True

    def move_robot_right(self):
        # TEST
        curr_joint_rotation = Simulator.total_rotations[self.curr_joint_rotation]
        if curr_joint_rotation == 0 and Simulator.firsts[self.curr_joint_rotation]:
            self.clockwise_selector.set_active(0)
            self.cw = 0
            Simulator.firsts[self.curr_joint_rotation] = False
        elif curr_joint_rotation < self.degree_quadrants[0]:
            self.clockwise_selector.set_active(1)
            self.cw = 1
        elif curr_joint_rotation < self.degree_quadrants[1]:
            self.clockwise_selector.set_active(1)
            self.cw = 1
        elif curr_joint_rotation < self.degree_quadrants[2]:
            self.clockwise_selector.set_active(0)
            self.cw = 0
        else:
            self.clockwise_selector.set_active(0)
            self.cw = 0

        self.rotate_joints(self.speed)

    def move_robot_left(self):
        # TEST
        curr_joint_rotation = Simulator.total_rotations[self.curr_joint_rotation]
        if curr_joint_rotation == 0 and Simulator.firsts[self.curr_joint_rotation]:
            self.clockwise_selector.set_active(1)
            self.cw = 1
            Simulator.firsts[self.curr_joint_rotation] = False
        elif curr_joint_rotation < self.degree_quadrants[0]:
            self.clockwise_selector.set_active(0)
            self.cw = 0
        elif curr_joint_rotation < self.degree_quadrants[1]:
            self.clockwise_selector.set_active(0)
            self.cw = 0
        elif curr_joint_rotation < self.degree_quadrants[2]:
            self.clockwise_selector.set_active(1)
            self.cw = 1
        else:
            self.clockwise_selector.set_active(1)
            self.cw = 1

        self.rotate_joints(self.speed)

    def move_robot_up(self):
        # TEST
        curr_joint_rotation = Simulator.total_rotations[self.curr_joint_rotation]
        if curr_joint_rotation < self.degree_quadrants[0] :
            self.clockwise_selector.set_active(0)
            self.cw = 0
        elif curr_joint_rotation < self.degree_quadrants[1]:
            self.clockwise_selector.set_active(1)
            self.cw = 1
        elif curr_joint_rotation < self.degree_quadrants[2]:
            self.clockwise_selector.set_active(1)
            self.cw = 1
        else:
            self.clockwise_selector.set_active(0)
            self.cw = 0

        self.rotate_joints(self.speed)

    def move_robot_down(self):
        # TEST
        curr_joint_rotation = Simulator.total_rotations[self.curr_joint_rotation]
        if curr_joint_rotation < self.degree_quadrants[0]:
            self.clockwise_selector.set_active(1)
            self.cw = 1
        elif curr_joint_rotation < self.degree_quadrants[1]:
            self.clockwise_selector.set_active(0)
            self.cw = 0
        elif curr_joint_rotation < self.degree_quadrants[2]:
            self.clockwise_selector.set_active(0)
            self.cw = 0
        else:
            self.clockwise_selector.set_active(1)
            self.cw = 1

        self.rotate_joints(self.speed)

    @staticmethod
    def handle_close(event):
        # Restart static variables
        Simulator.left_pressed = False
        Simulator.running = False

        Simulator.arm_limbs = []
        Simulator.arm_joints = []

        Simulator.total_rotations = [0, 0, 0]
        Simulator.unlocked = True

        Simulator.firsts = [True, True, True]

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
