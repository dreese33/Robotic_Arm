from time import sleep
from enum import Enum
import RPi.GPIO as gpio

class MotorStates(Enum):
    OFF = 1
    LOW = 2
    HIGH = 3

class StepperMotor():
    
    #Delay between motor steps
    currentDelay = 0.001
    
    """
    stepGpio: Gpio pin for step
    directionGpio: Gpio pin for direction
    stepsTaken: Total steps taken, refreshed after one second or specified time interval
    totalDelaysBeforeOneSecond: The total number of delays, refreshed after one second or specified time interval
    stepsFraction: Precalculated so the computer does not have to perform long division more than once
    delaysFraction: Precalculated so the computer does not have to perform long division more than once
    speed: Speed in steps per second to run the motor
    state: State the motor is currently in from MotorStates
    interval: Interval for which the motor will run until it restarts the number of delays
    """
    
    def __init__(self, stepGpio, directionGpio):
        self.stepGpio = stepGpio
        self.directionGpio = directionGpio
        
        self.totalDelaysBeforeInterval = 0
        self.stepsTaken = 0
        self.delayFraction = 0.0
        self.stepsFraction = 0.0
        
        self.speed = 0
        self.state = MotorStates.OFF
        self.interval = 1000.0
        
    #Starts motor, or simply changes its speed if it is already on
    def start(self, speed):
        self.speed = speed
        self.delaysRemaining = 0
        self.stepsFraction = 1.0 / speed
        self.delayFraction = 1.0 / self.interval   #1000 is the default interval
        
        if (self.state != MotorStates.OFF):
            return
        else:
            self.state = MotorStates.LOW
            
    #Restarts delays after interval is complete
    def restartDelaysRemaining(self):
        self.totalDelaysBeforeInterval = 0
        self.stepsTaken = 0
        
    #This function cannot be called in the high state
    #Untested
    def stopMotor(self):
        if (self.state != MotorStates.HIGH):
            self.state = MotorStates.OFF
            self.speed = 0
            restartDelaysRemaining()
        else:
            print("Do not call stopMotor() while the motor is in the middle of a step")
    
    #Sets the interval in milliseconds
    #Untested
    def setInterval(self, interval):
        if interval > 0:
            self.interval = interval
    
    #Runs motors for a number of degrees
    #Untested
    @staticmethod
    def runMotorsDegrees(self, motors, degrees):
        degreesToSteps = round(degrees * (5/9))
        runMotorsSteps(motors, degreesToSteps)
       
    #Runs the motors a number of steps
    #Untested
    @staticmethod
    def runMotorsSteps(self, motors, steps):
        if degreesToSteps == 0:
            return
        
        realStepsTaken = []
        
        if steps < 0:
            steps = -steps
            for motor in motors:
                gpio.output(motor.directionGpio, CCW)
                motor.restartDelaysRemaining()
                realStepsTaken.append(0)
        else:
            for motor in motors:
                gpio.output(motor.directionGpio, CW)
                motor.restartDelaysRemaining()
                realStepsTaken.append(0)
        
        while True:
            if (len(motors) == 0):
                break
            
            motorNumber = 0
            for motor in motors:
                if (realStepsTaken[motorNumber] >= steps):
                    motors.remove(motor)
                if (motor.totalDelaysBeforeInterval == motor.interval):
                    motor.restartDelaysRemaining()
                if (motor.state == MotorStates.LOW):
                    if ((motor.delayFraction * motor.totalDelaysBeforeInterval) >= (motor.stepsFraction * motor.stepsTaken)):
                        gpio.output(motor.stepGpio, gpio.HIGH)
                        motor.state = MotorStates.HIGH
                        motor.stepsTaken += 1.0
                        realStepsTaken[motorNumber] += 1
                    motor.totalDelaysBeforeInterval += 1.0
                elif (motor.state == MotorStates.HIGH):
                    gpio.output(motor.stepGpio, gpio.LOW)
                    motor.totalDelaysBeforeInterval += 1.0
                    motor.state = MotorStates.LOW
                motorNumber += 1
            sleep(StepperMotor.currentDelay)
            totalDelays += 1
            
        for motor in motors:
            motor.restartDelaysRemaining()
    
    #Runs the motors for a specified time interval in milliseconds
    #Untested
    @staticmethod
    def runMotorsTimeInterval(self, motors, timeInterval):
        if timeInterval <= 0:
            return
        
        for i in range(timeInterval):
            for motor in motors:
                if (motor.totalDelaysBeforeInterval == motor.interval):
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
            sleep(StepperMotor.currentDelay)
    
    #Runs the motors for their set interval
    #Untested
    @staticmethod
    def runMotorsInterval(self, motors):
        while True:
            if len(motors) == 0:
                break
            
            for motor in motors:
                if motor.totalDelayBeforeInterval == motor.interval:
                    motors.remove(motor)
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
            sleep(StepperMotor.currentDelay)
