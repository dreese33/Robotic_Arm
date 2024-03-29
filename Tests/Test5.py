from time import sleep
import RPi.GPIO as gpio
from StepperMotorControl.StepperMotor import StepperMotor
from StepperMotorControl.StepperMotor import MotorStates

directionGpio1 = 20
directionGpio2 = 12

stepGpio1 = 21
stepGpio2 = 16

CW = 0
CCW = 1

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

gpio.setup(directionGpio1, gpio.OUT)
gpio.setup(stepGpio1, gpio.OUT)
gpio.setup(directionGpio2, gpio.OUT)
gpio.setup(stepGpio2, gpio.OUT)

gpio.output(directionGpio1, CCW)
gpio.output(directionGpio2, CCW)

for i in range(200):
    gpio.output(stepGpio1, gpio.HIGH)
    gpio.output(stepGpio2, gpio.HIGH)
    sleep(0.0005)
    gpio.output(stepGpio1, gpio.LOW)
    gpio.output(stepGpio2, gpio.LOW)
    sleep(0.0005)

sleep(1)
gpio.output(directionGpio1, CW)
gpio.output(directionGpio2, CW)

for i in range(200):
    gpio.output(stepGpio1, gpio.HIGH)
    gpio.output(stepGpio2, gpio.HIGH)
    sleep(0.0005)
    gpio.output(stepGpio1, gpio.LOW)
    gpio.output(stepGpio2, gpio.LOW)
    sleep(0.0005)
