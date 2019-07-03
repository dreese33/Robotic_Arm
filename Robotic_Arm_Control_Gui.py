from tkinter import *
from ManualControlWheel import Robot_Manual_Control_Wheel
from tkinter import ttk
from RoboticArmSimulator import Simulator

window = Tk()

#Screen dimensions
screen_width = int(window.winfo_screenwidth() / 2)
screen_height = window.winfo_screenheight()

#Window definition
window.title("Robotic Arm Control")
window.geometry(str(screen_width) + "x" + str(screen_height))

#Tabs
tabControl = ttk.Notebook(window)

manualTab = ttk.Frame(tabControl)
tabControl.add(manualTab, text='Manual')

programRobotTab = ttk.Frame(tabControl)
tabControl.add(programRobotTab, text='Program')

armTab = ttk.Frame(tabControl)
tabControl.add(armTab, text='Arm')

tabControl.pack(expand=1, fill="both")

#Test out turtle graphics
canvasBase = Canvas(master = manualTab, width = int(screen_width / 2), height = int(screen_height / 2))
canvasBase.place(relx = 0.5, rely = 0.5, anchor = CENTER)

canvas_width = int(screen_width / 6)
canvas_height = int(screen_height / 6)

canvasWrist = Canvas(master = manualTab, width = canvas_width, height = canvas_height)
canvasWrist.place(relx = 0.05, rely = 0.05)

canvasElbow = Canvas(master = manualTab, width = canvas_width, height = canvas_height)
canvasElbow.place(relx = 0.78, rely = 0.05)

canvasShoulder = Canvas(master = manualTab, width = canvas_width, height = canvas_height)
canvasShoulder.place(relx = 0.78, rely = 0.78)

canvasClaw = Canvas(master = manualTab, width = canvas_width, height = canvas_height)
canvasClaw.place(relx = 0.05, rely = 0.78)

#Draw inner and outer circles for each individual joint
manualWheelBase = Robot_Manual_Control_Wheel.Robot_Manual_Control_Wheel(canvasBase, 'Base')
manualWheelWrist = Robot_Manual_Control_Wheel.Robot_Manual_Control_Wheel(canvasWrist, 'Wrist')
manualWheelElbow = Robot_Manual_Control_Wheel.Robot_Manual_Control_Wheel(canvasElbow, 'Elbow')
manualWheelShoulder = Robot_Manual_Control_Wheel.Robot_Manual_Control_Wheel(canvasShoulder, 'Shoulder')
manualWheelClaw = Robot_Manual_Control_Wheel.Robot_Manual_Control_Wheel(canvasClaw, 'Claw')

#Robotic arm simulator canvas
simulatorCanvas = Canvas(master = armTab, width = int(screen_width / 1.2), height = int(screen_width / 1.2))
simulatorCanvas.place(relx = 0.5, rely = 0.5, anchor = CENTER)
simulator = Simulator.Simulator(simulatorCanvas)

#Start
window.mainloop()