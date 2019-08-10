from StepperMotor import StepperMotor, MotorStates, Direction, Microstepping
from time import sleep
import RPi.GPIO as gpio

wrist_step = 16
elbow_step = 26
shoulder_step = 21

wrist_dir = 12
elbow_dir = 19
shoulder_dir = 20

wrist = StepperMotor(wrist_step, wrist_dir, Microstepping.SIXTEENTH, Direction.CW, 7)
elbow = StepperMotor(elbow_step, elbow_dir, Microstepping.SIXTEENTH, Direction.CW, 8)
shoulder = StepperMotor(shoulder_step, shoulder_dir, Microstepping.SIXTEENTH, Direction.CW, 8)

motors = [wrist, elbow, shoulder]

StepperMotor.step_motor_degrees(wrist, -90)
sleep(0.5)
StepperMotor.step_motors_degrees([elbow, shoulder], [30, 30])
for i in range(3):
    StepperMotor.step_motors_degrees([elbow, shoulder], [-60, -60])
    sleep(1)
    StepperMotor.step_motor_degrees(wrist, 30)
    StepperMotor.step_motor_degrees(wrist, -60)
    sleep(0.5)
    StepperMotor.step_motor_degrees(wrist, -30) #down
    StepperMotor.step_motors_degrees([elbow, shoulder], [-60, -60])
    sleep(1)
    StepperMotor.step_motor_degrees(wrist, 30)
    StepperMotor.step_motor_degrees(wrist, -60)
    sleep(0.5)
    StepperMotor.step_motor_degrees(wrist, -30) #down
StepperMotor.step_motors_degrees(motors, [-90, -30, -30])
