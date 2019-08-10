from tkinter import *
from ManualControlWheel.ManualControlWheel import ManualControlWheel
from tkinter import ttk
from RoboticArmSimulator.Simulator import Simulator
from StepperMotorControl.StepperMotor import StepperMotor, MotorStates, Direction, Microstepping
from ManualControlWheel.ManualControlWheel import ManualControlWheel


# Define gpio pins
wrist_step = 16
elbow_step = 26
shoulder_step = 21

wrist_dir = 12
elbow_dir = 19
shoulder_dir = 20

window = Tk()

screen_width = int(window.winfo_screenwidth() / 2)
screen_height = window.winfo_screenheight()

window.title("Robotic Arm Control")
window.geometry(str(screen_width) + "x" + str(screen_height))

tab_control = ttk.Notebook(window)

home_tab = ttk.Frame(tab_control)
tab_control.add(home_tab, text='Home')

manual_tab = ttk.Frame(tab_control)
tab_control.add(manual_tab, text='Manual')

program_robot_tab = ttk.Frame(tab_control)
tab_control.add(program_robot_tab, text='Program')

tab_control.pack(expand=1, fill="both")

canvas_base = Canvas(master=manual_tab, width=int(screen_width / 2), height=int(screen_height / 2))
canvas_base.place(relx=0.5, rely=0.5, anchor=CENTER)

canvas_width = int(screen_width / 6)
canvas_height = int(screen_height / 6)

canvas_wrist = Canvas(master=manual_tab, width=canvas_width, height=canvas_height)
canvas_wrist.place(relx=0.01, rely=0.03)

canvas_elbow = Canvas(master=manual_tab, width=canvas_width, height=canvas_height)
canvas_elbow.place(relx=0.80, rely=0.03)

canvas_shoulder = Canvas(master=manual_tab, width=canvas_width, height=canvas_height)
canvas_shoulder.place(relx=0.80, rely=0.77)

canvas_claw = Canvas(master=manual_tab, width=canvas_width, height=canvas_height)
canvas_claw.place(relx=0.01, rely=0.77)

# Define motors
motors = [StepperMotor(wrist_step, wrist_dir, Microstepping.SIXTEENTH, Direction.CCW, 7),
          StepperMotor(elbow_step, elbow_dir, Microstepping.SIXTEENTH, Direction.CCW, 7),
          StepperMotor(shoulder_step, shoulder_dir, Microstepping.SIXTEENTH, Direction.CCW, 8)]

# Add manual joint manipulation
ManualControlWheel(canvas_base, tab_control, -1, 'Base')
ManualControlWheel(canvas_wrist, tab_control, motors[0], 'Wrist')
ManualControlWheel(canvas_elbow, tab_control, motors[1], 'Elbow')
ManualControlWheel(canvas_shoulder, tab_control, motors[2], 'Shoulder')
ManualControlWheel(canvas_claw, tab_control, -1, 'Claw')

Simulator(motors)

window.mainloop()
