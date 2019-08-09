from time import sleep
import RPi.GPIO as gpio

stepGpio = 21
directionGpio = 20
stepGpio1 = 26
directionGpio1 = 19
stepGpio2 = 16
directionGpio2 = 12
CW = 0
CCW = 1

steps = 6400
steps_full = steps * 2

speed = 0.00001

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

#1

gpio.setup(directionGpio, gpio.OUT)
gpio.setup(stepGpio, gpio.OUT)

gpio.output(directionGpio, CCW)

#2
gpio.setup(directionGpio1, gpio.OUT)
gpio.setup(stepGpio1, gpio.OUT)

gpio.output(directionGpio1, CCW)

#3
gpio.setup(directionGpio2, gpio.OUT)
gpio.setup(stepGpio2, gpio.OUT)

gpio.output(directionGpio2, CCW)

for i in range(steps):
    gpio.output(stepGpio, gpio.HIGH)
    gpio.output(stepGpio1, gpio.HIGH)
    gpio.output(stepGpio2, gpio.HIGH)
    sleep(speed)
    gpio.output(stepGpio, gpio.LOW)
    gpio.output(stepGpio1, gpio.LOW)
    gpio.output(stepGpio2, gpio.LOW)
    sleep(speed)
    
sleep(0.5)
gpio.output(directionGpio, CW)
gpio.output(directionGpio1, CW)
gpio.output(directionGpio2, CW)
sleep(0.5)

for i in range(steps_full):
    gpio.output(stepGpio, gpio.HIGH)
    gpio.output(stepGpio1, gpio.HIGH)
    gpio.output(stepGpio2, gpio.HIGH)
    sleep(speed)
    gpio.output(stepGpio, gpio.LOW)
    gpio.output(stepGpio1, gpio.LOW)
    gpio.output(stepGpio2, gpio.LOW)
    sleep(speed)
    
sleep(0.5)
gpio.output(directionGpio, CCW)
gpio.output(directionGpio1, CCW)
gpio.output(directionGpio2, CCW)
sleep(0.5)

for i in range(steps_full):
    gpio.output(stepGpio, gpio.HIGH)
    gpio.output(stepGpio1, gpio.HIGH)
    gpio.output(stepGpio2, gpio.HIGH)
    sleep(speed)
    gpio.output(stepGpio, gpio.LOW)
    gpio.output(stepGpio1, gpio.LOW)
    gpio.output(stepGpio2, gpio.LOW)
    sleep(speed)
    
sleep(0.5)
gpio.output(directionGpio, CW)
gpio.output(directionGpio1, CW)
gpio.output(directionGpio2, CW)
sleep(0.5)

for i in range(steps_full):
    gpio.output(stepGpio, gpio.HIGH)
    gpio.output(stepGpio1, gpio.HIGH)
    gpio.output(stepGpio2, gpio.HIGH)
    sleep(speed)
    gpio.output(stepGpio, gpio.LOW)
    gpio.output(stepGpio1, gpio.LOW)
    gpio.output(stepGpio2, gpio.LOW)
    sleep(speed)
    
sleep(0.5)
gpio.output(directionGpio, CCW)
gpio.output(directionGpio1, CCW)
gpio.output(directionGpio2, CCW)
sleep(0.5)

for i in range(steps):
    gpio.output(stepGpio, gpio.HIGH)
    gpio.output(stepGpio1, gpio.HIGH)
    gpio.output(stepGpio2, gpio.HIGH)
    sleep(speed)
    gpio.output(stepGpio, gpio.LOW)
    gpio.output(stepGpio1, gpio.LOW)
    gpio.output(stepGpio2, gpio.LOW)
    sleep(speed)

