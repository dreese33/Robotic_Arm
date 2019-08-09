from time import sleep
import RPi.GPIO as gpio
from StepperMotorControl.StepperMotor import StepperMotor, MotorStates

direction_gpio1 = 20
direction_gpio2 = 12
direction_gpio3 = 19

step_gpio1 = 21
step_gpio2 = 16
step_gpio3 = 26

CW = 0
CCW = 1

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

gpio.setup(direction_gpio1, gpio.OUT)
gpio.setup(step_gpio1, gpio.OUT)
gpio.setup(direction_gpio2, gpio.OUT)
gpio.setup(step_gpio2, gpio.OUT)
gpio.setup(direction_gpio3, gpio.OUT)
gpio.setup(step_gpio3, gpio.OUT)

gpio.output(direction_gpio1, CCW)
gpio.output(direction_gpio2, CW)
gpio.output(direction_gpio3, CW)

motors = [StepperMotor(step_gpio1, direction_gpio1), StepperMotor(step_gpio2, direction_gpio2),
          StepperMotor(step_gpio3, direction_gpio3)]

motors[0].start(10000)
motors[1].start(10000)
motors[2].start(10000)

# Main loop
while True:
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

