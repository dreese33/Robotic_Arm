#Stepper motor abstraction classes
import threading
import RPi.GPIO as gpio
from time import sleep
import RepeatedTimer

class StepperMotorMultithreading():
    
    """
    Attributes:
        stepGpio: Gpio pin for step
        directionGpio: Gpio pin for direction
        identifier: String to identify the Motor
        speed: Speed to run the motor at in Steps/sec
        direction: Direction to spin motor
        timer: Threading timer
        stepsTaken: Steps taken by this motor so far
    """
    
    #Initializer
    def __init__(self, stepGpio, directionGpio, identifier):
        print("Hi")
        self.stepGpio = stepGpio
        self.directionGpio = directionGpio
        self.identifier = identifier
        self.timer = None
        
        gpio.setup(stepGpio, gpio.OUT)
        gpio.setup(directionGpio, gpio.OUT)
        
        self.speed = 0.0
        self.direction = 1
        self.stepsTaken = 0
        
        print("Initialized")
    
    #Reverse motor direction
    def reverseDirection(self):
        if (self.direction == 0):
            self.direction = 1
        else:
            self.direction = 0
            
    #Step the motor one time
    def stepMotor(self):
        print("Step")
        gpio.output(self.directionGpio, self.direction)
        gpio.output(self.stepGpio, gpio.HIGH)
        sleep(0.001)
        gpio.output(self.stepGpio, gpio.LOW)
        sleep(0.001)
        
    def startMotor(self):
        if self.timer != None:
            self.timer.start()
        else:
            print("Timer not assigned, use startMotor(speed) or startMotor(speed, direction)")
        
    def startMotor(self, speed):
        self.timer = RepeatedTimer.RepeatedTimer(1 / speed, self.stepMotor)
        
    def stopMotor(self):
        self.timer.stop()
        
    @classmethod
    def cleanupGpio(self):
        print("Cleaning up")
        gpio.cleanup()
    