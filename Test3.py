from time import sleep
import RPi.GPIO as gpio
from StepperMotorControl.StepperMotor import StepperMotor
from StepperMotorControl.StepperMotor import MotorStates

directionGpio1 = 20
directionGpio2 = 12
directionGpio3 = 19
#directionGpio4 = 6

stepGpio1 = 21
stepGpio2 = 16
stepGpio3 = 26
#stepGpio4 = 13

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
#gpio.setup(directionGpio4, gpio.OUT)
#gpio.setup(stepGpio4, gpio.OUT)

gpio.output(directionGpio1, CW)
gpio.output(directionGpio2, CW)
gpio.output(directionGpio3, CW)
#gpio.output(directionGpio4, CW)

#print("A")

motors = [StepperMotor(stepGpio1, directionGpio1), StepperMotor(stepGpio2, directionGpio2), StepperMotor(stepGpio3, directionGpio3)]

motors[0].start(50)
motors[1].start(50)
motors[2].start(50)

#print("Starting")

#Main test loop
totalDelays = 0
while True:
    motorNumber = 0
    for motor in motors:
        if (motor.totalDelaysBeforeInterval == 1000):
            #print("dasiofrhguidfngiudfnipugnuiodfgb")
            motor.restartDelaysRemaining()
            #print(str(motor.totalDelaysBeforeInterval) + " " + str(motor.stepsTaken))
        if (motor.state == MotorStates.LOW):
            #print(str(motor.stepsFraction * motor.stepsTaken) + " " + str(motor.delayFraction * motor.totalDelaysBeforeInterval))
            if ((motor.delayFraction * motor.totalDelaysBeforeInterval) >= (motor.stepsFraction * motor.stepsTaken)):
                #step, else delay motor
                gpio.output(motor.stepGpio, gpio.HIGH)
                motor.state = MotorStates.HIGH
                motor.stepsTaken += 1.0
                #print(str(motorNumber) + ": HIGH")
            motor.totalDelaysBeforeInterval += 1.0
        elif (motor.state == MotorStates.HIGH):
            gpio.output(motor.stepGpio, gpio.LOW)
            motor.totalDelaysBeforeInterval += 1.0
            motor.state = MotorStates.LOW
            #print(str(motorNumber) + ": LOW")
        motorNumber += 1
    sleep(StepperMotor.currentDelay)
    totalDelays += 1
    #print("Total Delays: " + str(totalDelays))