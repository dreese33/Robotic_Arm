from time import sleep
from enum import Enum
import RPi.GPIO as gpio


class MotorStates(Enum):
    OFF = 1
    LOW = 2
    HIGH = 3


class StepperMotor:
    
    # Delay between motor steps
    currentDelay = 0.001
    CW = 0
    CCW = 1
    
    """
    step_gpio: Gpio pin for step
    direction_gpio: Gpio pin for direction
    steps_taken: Total steps taken, refreshed after one second or specified time interval
    total_delays_before_interval: The total number of delays, refreshed after one second or specified time interval
    steps_fraction: Precalculated so the computer does not have to perform long division more than once
    delays_fraction: Precalculated so the computer does not have to perform long division more than once
    speed: Speed in steps per second to run the motor
    state: State the motor is currently in from MotorStates
    interval: Interval for which the motor will run until it restarts the number of delays
    CW: clockwise
    CCW: counterclockwise
    """
    
    def __init__(self, step_gpio, direction_gpio):
        self.step_gpio = step_gpio
        self.direction_gpio = direction_gpio
        
        self.total_delays_before_interval = 0
        self.steps_taken = 0
        self.delay_fraction = 0.0
        self.steps_fraction = 0.0
        
        self.speed = 0
        self.state = MotorStates.OFF
        self.interval = 1000.0
        
    # Starts motor, or simply changes its speed if it is already on
    def start(self, speed):
        self.speed = speed
        self.steps_fraction = 1.0 / speed
        self.delay_fraction = 1.0 / self.interval   # 1000 is the default interval
        
        if self.state != MotorStates.OFF:
            return
        else:
            self.state = MotorStates.LOW
            
    # Restarts delays after interval is complete
    def restart_delays_remaining(self):
        self.total_delays_before_interval = 0
        self.steps_taken = 0

    # This function cannot be called in the high state
    # Untested
    def stop_motor(self):
        if self.state != MotorStates.HIGH:
            self.state = MotorStates.OFF
            self.speed = 0
            self.restart_delays_remaining()
        else:
            print("Do not call stopMotor() while the motor is in the middle of a step")
    
    # Sets the interval in milliseconds
    # Untested
    def set_interval(self, interval):
        if interval > 0:
            self.interval = interval
    
    # Runs motors for a number of degrees
    # Untested
    @staticmethod
    def run_motors_degrees(motors, degrees):
        degrees_to_steps = round(degrees * (5/9))
        StepperMotor.run_motors_steps(motors, degrees_to_steps)
       
    # Runs the motors a number of steps
    # Untested
    @staticmethod
    def run_motors_steps(motors, steps):
        if steps == 0:
            return
        
        real_steps_taken = []
        
        if steps < 0:
            steps = -steps
            for motor in motors:
                gpio.output(motor.direction_gpio, StepperMotor.CCW)
                motor.restart_delays_remaining()
                real_steps_taken.append(0)
        else:
            for motor in motors:
                gpio.output(motor.direction_gpio, StepperMotor.CW)
                motor.restart_delays_remaining()
                real_steps_taken.append(0)
        
        while True:
            if len(motors) == 0:
                break
            
            motor_number = 0
            for motor in motors:
                if real_steps_taken[motor_number] >= steps:
                    motors.remove(motor)
                if motor.total_delays_before_interval == motor.interval:
                    motor.restart_delays_remaining()
                if motor.state == MotorStates.LOW:
                    if (motor.delay_fraction * motor.total_delays_before_interval) >= \
                            (motor.steps_fraction * motor.steps_taken):
                        gpio.output(motor.stepGpio, gpio.HIGH)
                        motor.state = MotorStates.HIGH
                        motor.steps_taken += 1.0
                        real_steps_taken[motor_number] += 1
                    motor.total_delays_before_interval += 1.0
                elif motor.state == MotorStates.HIGH:
                    gpio.output(motor.step_gpio, gpio.LOW)
                    motor.total_delays_before_interval += 1.0
                    motor.state = MotorStates.LOW
                motor_number += 1
                motor.total_delays_before_interval += 1
            sleep(StepperMotor.currentDelay)
            
        for motor in motors:
            motor.restart_delays_remaining()

    # Runs the motors for a specified time interval in milliseconds
    # Untested
    @staticmethod
    def run_motors_time_interval(motors, time_interval):
        if time_interval <= 0:
            return
        
        for i in range(time_interval):
            for motor in motors:
                if motor.total_delays_before_interval == motor.interval:
                    motor.restart_delays_remaining()
                if motor.state == MotorStates.LOW:
                    if (motor.delay_fraction * motor.total_delays_before_interval) \
                            >= (motor.steps_fraction * motor.steps_taken):
                        gpio.output(motor.step_gpio, gpio.HIGH)
                        motor.state = MotorStates.HIGH
                        motor.steps_taken += 1.0
                    motor.total_delays_before_interval += 1.0
                elif motor.state == MotorStates.HIGH:
                    gpio.output(motor.step_gpio, gpio.LOW)
                    motor.total_delays_before_interval += 1.0
                    motor.state = MotorStates.LOW
            sleep(StepperMotor.currentDelay)
    
    # Runs the motors for their set interval
    # Untested
    @staticmethod
    def run_motors_interval(motors):
        while True:
            if len(motors) == 0:
                break
            
            for motor in motors:
                if motor.total_delays_before_interval == motor.interval:
                    motors.remove(motor)
                if motor.state == MotorStates.LOW:
                    if (motor.delay_fraction * motor.total_delays_before_interval) \
                            >= (motor.steps_fraction * motor.steps_taken):
                        gpio.output(motor.step_gpio, gpio.HIGH)
                        motor.state = MotorStates.HIGH
                        motor.steps_taken += 1.0
                    motor.total_delays_before_interval += 1.0
                elif motor.state == MotorStates.HIGH:
                    gpio.output(motor.step_gpio, gpio.LOW)
                    motor.total_delays_before_interval += 1.0
                    motor.state = MotorStates.LOW
            sleep(StepperMotor.currentDelay)
