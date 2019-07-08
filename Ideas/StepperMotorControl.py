# Work in progress for modifying motors, code has not been tested yet at all

from time import sleep
import RPi.GPIO as gpio
from Ideas.Motor import Motor

# Motor definition arrays
motors = []
motor_identifiers = []
run_motors = False

# Motors ready to step
ready_motors = []

# Setup basic gpio
gpio.setmode(gpio.BCM)


# Removes all motors
def remove_all():
    global motors, motor_identifiers, run_motors

    motors = []
    motor_identifiers = []
    run_motors = False
    gpio.cleanup()


# Removes motor from list of motors
def remove_motor(motor_identifier):
    if motor_identifier in motor_identifiers:
        index = motor_identifiers.index(motor_identifier)
        motor_identifiers.pop(index)
        motors.pop(index)
    else:
        print("Motor does not exist")


# Adds motor to the list of motors
def add_motor(motor_step, motor_direction, motor_identifier):
    motors.append(Motor(motor_step, motor_direction, motor_identifier))
    motor_identifiers.append(motor_identifier)
    gpio.setup(motor_step, gpio.OUT)
    gpio.setup(motor_direction, gpio.OUT)


# Move motor at specified speed in steps per second
def start_motor(motor_identifier, motor_speed, motor_direction):
    if motor_identifier in motor_identifiers:
        index = motor_identifiers.index(motor_identifier)
        current_motor = motors[index]
        current_motor.speed = motor_speed
        current_motor.run = True
        current_motor.direction = motor_direction
        motors[index] = current_motor
    else:
        print("Motor does not exist")


# Stop specified motor from running
def stop_motor(motor_identifier):
    if motor_identifier in motor_identifiers:
        index = motor_identifiers.index(motor_identifier)
        motors[index].run = False
    else:
        print("Motor does not exist")


# Stop all motors from running
def stop_motors():
    global run_motors
    run_motors = False


# Returns the motor with the lowest speed
def slowest_running_motor():
    slowest = motors[0]
    for motor in motors:
        if slowest.speed > motor.speed:
            slowest = motor
    return slowest


# Returns the motor with the highest speed
def fastest_running_motor():
    fastest = motors[0]
    for motor in motors:
        if fastest.speed < motor.speed:
            fastest = motor
    return fastest


# Updates each motor
def update_motors():
    for motor in motors:
        motor.timeUntilRun -= 1
        if motor.timeUntilRun == 0:
            ready_motors.append(motor)


# Calculates time until next run
def calculate_time_until_next_run():
    pass


def stop():
    global run_motors
    run_motors = False


# Begin running started motors
# This will be run on one thread, and another thread will run the code to control this
def start():
    global run_motors
    run_motors = True
    while run_motors:
        if len(motors) == 0:
            run_motors = False
            break
        if len(ready_motors) == 0:
            sleep(0.001)
            update_motors()
            continue
        for currMotor in ready_motors:
            gpio.output(currMotor.directionGpio, currMotor.direction)
            gpio.output(currMotor.stepGpio, gpio.HIGH)

            # Incomplete library, use newer stepper motor library to control motors
            # motor = motors[motor_identifiers.index(currMotor.identifier)]
            # motor.timeUntilRun = calculate_time_until_next_run(currMotor)
        """
        for motor in motors:
            if motor.run:
                if motor.timeUntilRun == 0:
                    #Setup motor and direction
                    motor.timeUntilRun = calculateTimeUntilNextRun(motor)
                    gpio.output(motor.directionGpio, motor.direction)
                    
                #else:
                    #motor.timeUntilRun -= 1"""
