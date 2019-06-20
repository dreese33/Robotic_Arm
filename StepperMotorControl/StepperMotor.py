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
    delaysRemaining: Number of delays until the motors state is set to HIGH
    speed: Speed in steps per second to run the motor
    state: State the motor is currently in from MotorStates
    """
    
    def __init__(self, stepGpio, directionGpio):
        self.stepGpio = stepGpio
        self.directionGpio = directionGpio
        self.delaysRemaining = 0
        self.speed = 0
        self.state = MotorStates.OFF
        
    def start(self, speed):
        self.speed = speed
        self.delaysRemaining = 0
        
        if (self.state != MotorStates.OFF):
            return
        else:
            self.state = MotorStates.LOW
            
    def restartDelaysRemaining(self):
        pass