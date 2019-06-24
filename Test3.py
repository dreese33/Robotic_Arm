from time import sleep
import RPi.GPIO as gpio
from StepperMotorControl.StepperMotor import StepperMotor
from StepperMotorControl.StepperMotor import MotorStates

directionGpio1 = 20
directionGpio2 = 12
directionGpio3 = 19

stepGpio1 = 21
stepGpio2 = 16
stepGpio3 = 26

CW = 0
CCW = 1

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

gpio.setup(directionGpio1, gpio.OUT)
gpio.setup(stepGpio1, gpio.OUT)
gpio.setup(directionGpio2, gpio.OUT)
gpio.setup(stepGpio2, gpio.OUT)
gpio.setup(directionGpio3, gpio.OUT)
gpio.setup(stepGpio3, gpio.OUT)

gpio.output(directionGpio1, CCW)
gpio.output(directionGpio2, CW)
gpio.output(directionGpio3, CW)

motors = [StepperMotor(stepGpio1, directionGpio1), StepperMotor(stepGpio2, directionGpio2), StepperMotor(stepGpio3, directionGpio3)]

motors[0].start(10000)
motors[1].start(10000)
motors[2].start(10000)

#Main test loop
totalDelays = 0
while True:
    motorNumber = 0
    for motor in motors:
        if (motor.totalDelaysBeforeInterval == 1000):
            motor.restartDelaysRemaining()
        if (motor.state == MotorStates.LOW):
            if ((motor.delayFraction * motor.totalDelaysBeforeInterval) >= (motor.stepsFraction * motor.stepsTaken)):
                gpio.output(motor.stepGpio, gpio.HIGH)
                motor.state = MotorStates.HIGH
                motor.stepsTaken += 1.0
            motor.totalDelaysBeforeInterval += 1.0
        elif (motor.state == MotorStates.HIGH):
            gpio.output(motor.stepGpio, gpio.LOW)
            motor.totalDelaysBeforeInterval += 1.0
            motor.state = MotorStates.LOW
        motorNumber += 1
    sleep(StepperMotor.currentDelay)
    totalDelays += 1