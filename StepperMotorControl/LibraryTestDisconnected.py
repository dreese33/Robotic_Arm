from StepperMotor import StepperMotor, MotorStates, Direction, Microstepping
from time import sleep
import RPi.GPIO as gpio

"""
Motor definitions
"""
test_step_pin = 21
test_direction_pin = 20

motor_one_cw = StepperMotor(test_step_pin, test_direction_pin, Microstepping.ONE, Direction.CW)
motor_one_ccw = StepperMotor(test_step_pin, test_direction_pin, Microstepping.ONE, Direction.CCW)
motor_halfa_cw = StepperMotor(test_step_pin, test_direction_pin, Microstepping.HALFA, Direction.CW)
motor_halfa_ccw = StepperMotor(test_step_pin, test_direction_pin, Microstepping.HALFA, Direction.CCW)
motor_halfb_cw = StepperMotor(test_step_pin, test_direction_pin, Microstepping.HALFB, Direction.CW)
motor_halfb_ccw = StepperMotor(test_step_pin, test_direction_pin, Microstepping.HALFB, Direction.CCW)
motor_quarter_cw = StepperMotor(test_step_pin, test_direction_pin, Microstepping.QUARTER, Direction.CW)
motor_quarter_ccw = StepperMotor(test_step_pin, test_direction_pin, Microstepping.QUARTER, Direction.CCW)
motor_eighth_cw = StepperMotor(test_step_pin, test_direction_pin, Microstepping.EIGHTH, Direction.CW)
motor_eighth_ccw = StepperMotor(test_step_pin, test_direction_pin, Microstepping.EIGHTH, Direction.CCW)
motor_sixteenth_cw = StepperMotor(test_step_pin, test_direction_pin, Microstepping.SIXTEENTH, Direction.CW)
motor_sixteenth_ccw = StepperMotor(test_step_pin, test_direction_pin, Microstepping.SIXTEENTH, Direction.CCW)
motor_thirtysecond_cw = StepperMotor(test_step_pin, test_direction_pin, Microstepping.THIRTYSECOND, Direction.CW)
motor_thirtysecond_ccw = StepperMotor(test_step_pin, test_direction_pin, Microstepping.THIRTYSECOND, Direction.CCW)

motor_array = [motor_one_cw, motor_one_ccw, motor_halfa_cw, motor_halfa_ccw, motor_halfb_cw, motor_halfb_ccw, 
               motor_quarter_cw, motor_quarter_ccw, motor_eighth_cw, motor_eighth_ccw, motor_sixteenth_cw,
               motor_sixteenth_ccw, motor_thirtysecond_cw, motor_thirtysecond_ccw]

"""
Gpio setup + microstepping tests (also tests get_time)
"""
def test_motor_disconnected(motor):
    gpio.output(motor.step_gpio, gpio.HIGH)
    assert motor.get_time() == StepperMotor.currentDelayTB6600[motor.current_microstepping.value]
    sleep(motor.get_time())
    gpio.output(motor.step_gpio, gpio.LOW)
    
for i in motor_array:
    test_motor_disconnected(i)


"""
Tests start, restart_delays_remaining, set_interval
"""
def test_motor_start(motor):
    assert motor.start(-45) == "Cannot start motor with speed <= 0"
    assert motor.start(0) == "Cannot start motor with speed <= 0"
    
    motor.start(100)
    assert motor.speed == 100
    assert motor.steps_fraction == 1.0 / motor.speed
    assert motor.delay_fraction == 1.0 / motor.interval
    assert motor.state == MotorStates.LOW
    
def test_motor_delays_remaining(motor):
    motor.start(100)
    motor.restart_delays_remaining()
    assert motor.total_delays_before_interval == 0
    assert motor.steps_taken == 0
    
def test_motor_set_interval(motor):
    assert motor.set_interval(0) == "Interval <= 0"
    assert motor.set_interval(-100) == "Interval <= 0"
    motor.set_interval(693)
    assert motor.interval == 693
    
for i in motor_array:
    test_motor_start(i)
    test_motor_delays_remaining(i)
    test_motor_set_interval(i)
    
    
"""
Test get_microstepping_factor
"""
def test_get_microstepping_factor(motor):
    assert motor.get_microstepping_factor(Microstepping.ONE) == 1
    assert motor.get_microstepping_factor(Microstepping.HALFA) == 2
    assert motor.get_microstepping_factor(Microstepping.HALFB) == 2
    assert motor.get_microstepping_factor(Microstepping.QUARTER) == 4
    assert motor.get_microstepping_factor(Microstepping.EIGHTH) == 8
    assert motor.get_microstepping_factor(Microstepping.SIXTEENTH) == 16
    assert motor.get_microstepping_factor(Microstepping.THIRTYSECOND) == 32
    
for i in motor_array:
    test_get_microstepping_factor(i)