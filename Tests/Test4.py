from time import sleep
import RPi.GPIO as gpio

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

for i in range(200):
    gpio.output(step_gpio1, gpio.HIGH)
    gpio.output(step_gpio2, gpio.HIGH)
    gpio.output(step_gpio3, gpio.HIGH)
    sleep(0.005)
    gpio.output(step_gpio1, gpio.LOW)
    gpio.output(step_gpio2, gpio.LOW)
    gpio.output(step_gpio3, gpio.LOW)
    sleep(0.005)

sleep(1)
gpio.output(direction_gpio1, CW)
gpio.output(direction_gpio2, CCW)
gpio.output(direction_gpio3, CCW)

for i in range(200):
    gpio.output(step_gpio1, gpio.HIGH)
    gpio.output(step_gpio2, gpio.HIGH)
    gpio.output(step_gpio3, gpio.HIGH)
    sleep(0.005)
    gpio.output(step_gpio1, gpio.LOW)
    gpio.output(step_gpio2, gpio.LOW)
    gpio.output(step_gpio3, gpio.LOW)
    sleep(0.005)
