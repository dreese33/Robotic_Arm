# Stepper motor abstraction classes
import RPi.GPIO as gpio
from time import sleep
from StepperMotorMultithreaded.RepeatedTimer import RepeatedTimer


class StepperMotorMultithreading:
    
    """
    Attributes:
        step_gpio: Gpio pin for step
        direction_gpio: Gpio pin for direction
        identifier: String to identify the Motor
        speed: Speed to run the motor at in Steps/sec
        direction: Direction to spin motor
        timer: Threading timer
        steps_taken: Steps taken by this motor so far
    """
    
    # Initializer
    def __init__(self, step_gpio, direction_gpio, identifier):
        self.step_gpio = step_gpio
        self.direction_gpio = direction_gpio
        self.identifier = identifier
        self.timer = None
        
        gpio.setup(step_gpio, gpio.OUT)
        gpio.setup(direction_gpio, gpio.OUT)
        
        self.speed = 0.0
        self.direction = 1
        self.steps_taken = 0
    
    # Reverse motor direction
    def reverse_direction(self):
        if self.direction == 0:
            self.direction = 1
        else:
            self.direction = 0
            
    # Step the motor one time
    def step_motor(self):
        gpio.output(self.direction_gpio, self.direction)
        gpio.output(self.step_gpio, gpio.HIGH)
        sleep(0.001)
        gpio.output(self.step_gpio, gpio.LOW)
        sleep(0.001)
        
    def start(self):
        if self.timer is not None:
            self.timer.start()
        else:
            print("Timer not assigned, use startMotor(speed) or startMotor(speed, direction)")
        
    def start_motor(self, speed):
        self.timer = RepeatedTimer(1 / speed, self.step_motor)
        
    def stop_motor(self):
        self.timer.stop()
        
    @staticmethod
    def cleanup_gpio():
        print("Cleaning up")
        gpio.cleanup()
