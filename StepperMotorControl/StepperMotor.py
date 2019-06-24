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
        
    #Starts motor, or simply changes its speed if it is already on
    def start(self, speed):
        self.speed = speed
        self.delaysRemaining = 0
        self.stepsFraction = 1.0 / speed
        self.delayFraction = 1.0 / 1000.0   #1000 is the one second interval for the motor to run
        
        if (self.state != MotorStates.OFF):
            return
        else:
            self.state = MotorStates.LOW
            
    def restartDelaysRemaining(self):
        self.totalDelaysBeforeInterval = 0
        self.stepsTaken = 0
        
    #This function cannot be called in the high state
    def stopMotor(self):
        if (self.state != MotorStates.HIGH):
            self.state = MotorStates.OFF
            self.speed = 0
            restartDelaysRemaining()
        else:
            print("Do not call stopMotor() while the motor is in the middle of a step")
