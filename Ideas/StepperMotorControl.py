#Work in progress for modifying motors, code has not been tested yet at all

from time import sleep
import RPi.GPIO as gpio
import Motor

#Motor definition arrays
motors = []
motorIdentifiers = []
runMotors = False

#Motors ready to step
readyMotors = []

#Setup basic gpio
gpio.setmode(gpio.BCM)

#Removes all motors
def removeAll():
    motors = []
    motorIdentifiers = []
    runMotors = False
    gpio.cleanup()

#Removes motor from list of motors
def removeMotor(motorIdentifier):
    if motorIdentifier in motorIdentifiers:
        index = motorIdentifiers.index(motorIdentifier)
        motorIdentifiers.pop(index)
        motors.pop(index)
    else:
        print("Motor does not exist")

#Adds motor to the list of motors
def addMotor(motorStep, motorDirection, motorIdentifier):
    motors.append(Motor(motorStep, motorDirection, motorIdentifier))
    motorIdentifiers.append(motorIdentifier)
    gpio.setup(motorStep, gpio.OUT)
    gpio.setup(motorDirection, gpio.OUT)

#Move motor at specified speed in steps per second
def startMotor(motorIdentifier, motorSpeed, motorDirection):
    if motorIdentifier in motorIdentifiers:
        index = motorIdentifiers.index(motorIdentifier)
        currentMotor = motors[index]
        currentMotor.speed = motorSpeed
        currentMotor.run = True
        currentMotor.direction = motorDirection
        motors[index] = currentMotor
    else:
        print("Motor does not exist")
        
#Stop specified motor from running
def stopMotor(motorIdentifier):
    if motorIdentifier in motorIdentifiers:
        index = motorIdentifiers.index(motorIdentifier)
        motors[index].run = False
    else:
        print("Motor does not exist")
        
#Stop all motors from running
def stopMotors():
    runMotors = False
       
#Returns the motor with the lowest speed
def lowestSpeedRunningMotor():
    slowest = motors[0]
    for motor in motors:
        if slowest.speed > motor.speed:
            slowest = motor
    return slowest

#Returns the motor with the highest speed
def highestSpeedRunningMotor():
    fastest = motors[0]
    for motor in motors:
        if fastest.speed < motor.speed:
            fastest = motor
    return fastest
    
#Updates each motor
def updateMotors():
    timeCounter += 1
    for motor in motors:
        motor.timeUntilRun -= 1
        if (motor.timeUntilRun == 0):
            readyMotors.append(motor)
    
#Calculates time until next run
def calculateTimeUntilNextRun(motor):
    pass
       
def stop():
    runMotors = False
       
#Begin running started motors
#This will be run on one thread, and another thread will run the code to control this
def start():
    runMotors = True
    while(runMotors):
        if len(motors) == 0:
            runMotors = False
            break
        if len(readyMotors) == 0:
            sleep(0.001)
            updateMotors()
            continue
        for currMotor in readyMotors:
            gpio.output(currMotor.directionGpio, currMotor.direction)
            gpio.output(currMotor.stepGpio, gpio.HIGH)
            motor = motors[motorIdentifiers.index(currMotor.identifier)]
            motor.timeUntilRun = calculateTimeUntilNextRun(currMotor)
        """
        for motor in motors:
            if motor.run:
                if motor.timeUntilRun == 0:
                    #Setup motor and direction
                    motor.timeUntilRun = calculateTimeUntilNextRun(motor)
                    gpio.output(motor.directionGpio, motor.direction)
                    
                #else:
                    #motor.timeUntilRun -= 1"""
