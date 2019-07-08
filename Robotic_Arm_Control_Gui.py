from tkinter import *
from ManualControlWheel.ManualControlWheel import ManualControlWheel
from tkinter import ttk
from RoboticArmSimulator import Simulator

window = Tk()

screen_width = int(window.winfo_screenwidth() / 2)
screen_height = window.winfo_screenheight()

window.title("Robotic Arm Control")
window.geometry(str(screen_width) + "x" + str(screen_height))

tab_control = ttk.Notebook(window)

manual_tab = ttk.Frame(tab_control)
tab_control.add(manual_tab, text='Manual')

program_robot_tab = ttk.Frame(tab_control)
tab_control.add(program_robot_tab, text='Program')

arm_tab = ttk.Frame(tab_control)
tab_control.add(arm_tab, text='Arm')

tab_control.pack(expand=1, fill="both")

canvas_base = Canvas(master=manual_tab, width=int(screen_width / 2), height=int(screen_height / 2))
canvas_base.place(relx=0.5, rely=0.5, anchor=CENTER)

canvas_width = int(screen_width / 6)
canvas_height = int(screen_height / 6)

canvas_wrist = Canvas(master=manual_tab, width=canvas_width, height=canvas_height)
canvas_wrist.place(relx=0.05, rely=0.05)

canvas_elbow = Canvas(master=manual_tab, width=canvas_width, height=canvas_height)
canvas_elbow.place(relx=0.78, rely=0.05)

canvas_shoulder = Canvas(master=manual_tab, width=canvas_width, height=canvas_height)
canvas_shoulder.place(relx=0.78, rely=0.78)

canvas_claw = Canvas(master=manual_tab, width=canvas_width, height=canvas_height)
canvas_claw.place(relx=0.05, rely=0.78)

# Add manual joint manipulation
ManualControlWheel(canvas_base, 'Base')
ManualControlWheel(canvas_wrist, 'Wrist')
ManualControlWheel(canvas_elbow, 'Elbow')
ManualControlWheel(canvas_shoulder, 'Shoulder')
ManualControlWheel(canvas_claw, 'Claw')

simulator_canvas = Canvas(master=arm_tab, width=int(screen_width / 1.2), height=int(screen_width / 1.2))
simulator_canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
simulator = Simulator.Simulator(simulator_canvas)

window.mainloop()
