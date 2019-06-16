from time import sleep
import RPi.GPIO as gpio
from pynput.keyboard import Controller, Key, Listener

#Pin definitions
directionLarge = 20  #CW+
stepLarge = 21      #CLK+
directionSmall = 12  #CW+
stepSmall = 16       #CLK+
CW = 1    #clockwise
CCW = 0   #counter clockwise

#Delay increment
delayIncrement = 0.001

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

gpio.setup(directionLarge, gpio.OUT)
gpio.setup(stepLarge, gpio.OUT)
gpio.setup(directionSmall, gpio.OUT)
gpio.setup(stepSmall, gpio.OUT)

gpio.output(directionLarge, CW)
gpio.output(directionSmall, CW)

def on_press(key):
    print(format(key))
    
def runRotation():
    #Moves both motors 200 steps
    for i in range(200):
        gpio.output(stepLarge, gpio.HIGH)
        gpio.output(stepSmall, gpio.HIGH)
        sleep(delayIncrement)
        gpio.output(stepLarge, gpio.LOW)
        gpio.output(stepSmall, gpio.LOW)
        sleep(delayIncrement)
    sleep(1)
    
def runForward():
    gpio.output(directionLarge, CW)
    gpio.output(directionSmall, CW)
    runRotation()
    
def runBack():
    gpio.output(directionLarge, CCW)
    gpio.output(directionSmall, CCW)
    runRotation()
    
def on_release(key):
    if key == Key.esc:
        return False
    if key == Key.left:
        runForward()
    if key == Key.right:
        runBack()
    
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()