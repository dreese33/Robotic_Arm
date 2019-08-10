from StepperMotor import StepperMotor, MotorStates, Direction, Microstepping
from time import sleep
import RPi.GPIO as gpio

"""
Motor definitions
"""
test_step_pin = 21
test_direction_pin = 20

test_step_pin1 = 26
test_direction_pin1 = 19

test_step_pin2 = 16
test_direction_pin2 = 12

"""
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

motor_sixteenth_ccw = StepperMotor(test_step_pin, test_direction_pin, Microstepping.SIXTEENTH, Direction.CCW, 8)
motor_sixteenth_cw = StepperMotor(test_step_pin1, test_direction_pin1, Microstepping.SIXTEENTH, Direction.CW, 8)
motor_sixteenth_cw1 = StepperMotor(test_step_pin2, test_direction_pin2, Microstepping.SIXTEENTH, Direction.CW, 7)

"""
def test_step_motors_steps1(motor):
    assert motor.step_motors_steps(motor, 0) == "Steps cannot be 0"
    
    motor.start(50)
    motor.run_motors_steps([motor], 45)
    
test_run_motors_steps1(motor_one_cw)
"""


"""
Testing methods to run a single motor
"""
def test_step_motor(motor):
    motor.start(50)
    assert motor.step_motor(0) == "Cannot step 0 times"
    #motor.step_motor_degrees(90)
    #sleep(0.5)
    motor.step_motor_degrees(40)
    
def test_step_motor_reverse(motor):
    motor.start(50)
    motor.step_motor_degrees(-40)
    
def test_two_motors_same_speed(motors):
    StepperMotor.step_motors_degrees(motors, [30, -30])
    
def test_two_motors_same_speed_reverse(motors):
    StepperMotor.step_motors_degrees(motors, [-30, 30])
    
motors = [motor_sixteenth_cw, motor_sixteenth_ccw, motor_sixteenth_cw1]
""" Test 1
test_step_motor(motor_sixteenth_cw)
test_step_motor(motor_sixteenth_ccw)
sleep(0.5)
test_step_motor_reverse(motor_sixteenth_cw)
test_step_motor_reverse(motor_sixteenth_ccw)"""

""" Test 2
test_two_motors_same_speed([motor_sixteenth_cw, motor_sixteenth_ccw])
motor_sixteenth_ccw.reverse_direction()
sleep(0.5)
test_two_motors_same_speed_reverse([motor_sixteenth_cw, motor_sixteenth_ccw])
"""

# Test motors at different steps
#StepperMotor.step_motors_degrees(motors, [30, -120])
#StepperMotor.step_motors_degrees(motors, [-30, 15])
#StepperMotor.step_motors_degrees(motors, [0, 0])

"""
StepperMotor.step_motors_degrees(motors, [30, -120])
StepperMotor.step_motor_degrees(motor_sixteenth_ccw, -90)
StepperMotor.step_motor_degrees(motor_sixteenth_ccw, -90)
StepperMotor.step_motors_degrees(motors, [-30, -120])
StepperMotor.step_motors_degrees(motors, [30, 120])"""

#StepperMotor.step_motors_degrees(motors, [-30, -120])
"""
first = True
for i in range(3):
    if first:
        StepperMotor.step_motors_degrees(motors, [30, -30, 30])
        first = False
    else:
        StepperMotor.step_motors_degrees(motors, [30, 30, 30])
    StepperMotor.step_motors_degrees(motors, [-30, -30, 30])
    StepperMotor.step_motors_degrees(motors, [30, 30, 30])
    StepperMotor.step_motors_degrees(motors, [-30, -30, 30])"""
#motor_sixteenth_cw1.step_motor_degrees(360)

"""
Testing step_motors_micro, step_degrees_micro
"""
StepperMotor.step_motors_degrees(motors, [54, 54, 54])
#StepperMotor.step_motors_micro(motors, [30, 30, 30])