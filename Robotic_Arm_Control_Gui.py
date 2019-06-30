from tkinter import *
from ManualControlWheel import Robot_Manual_Control_Wheel
from tkinter import ttk

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
canvas = Canvas(master = manualTab, width = int(screen_width / 2), height = int(screen_height / 2))
canvas.place(relx = 0.5, rely = 0.5, anchor = CENTER)

#Draw inner and outer circles
manualWheelBase = Robot_Manual_Control_Wheel.Robot_Manual_Control_Wheel(canvas, screen_width, screen_height)

#Start
window.mainloop()