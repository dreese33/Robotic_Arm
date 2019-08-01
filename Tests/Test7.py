from time import sleep
import RPi.GPIO as gpio

stepGpio = 21
directionGpio = 20

speed = 0.0003
steps = 6400
steps_full = steps * 2
CW = 0
CCW = 1

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

#1
gpio.setup(directionGpio, gpio.OUT)
gpio.setup(stepGpio, gpio.OUT)

gpio.output(directionGpio, CCW)

for i in range(steps):
    gpio.output(stepGpio, gpio.HIGH)
    sleep(speed)
    gpio.output(stepGpio, gpio.LOW)
    sleep(speed)
    
sleep(0.5)
gpio.output(directionGpio, CW)
sleep(0.5)

for i in range(steps_full):
    gpio.output(stepGpio, gpio.HIGH)
    sleep(speed)
    gpio.output(stepGpio, gpio.LOW)
    sleep(speed)
    
sleep(0.5)
gpio.output(directionGpio, CCW)
sleep(0.5)

for i in range(steps_full):
    gpio.output(stepGpio, gpio.HIGH)
    sleep(speed)
    gpio.output(stepGpio, gpio.LOW)
    sleep(speed)
    
sleep(0.5)
gpio.output(directionGpio, CW)
sleep(0.5)

for i in range(steps_full):
    gpio.output(stepGpio, gpio.HIGH)
    sleep(speed)
    gpio.output(stepGpio, gpio.LOW)
    sleep(speed)
    
sleep(0.5)
gpio.output(directionGpio, CCW)
sleep(0.5)

for i in range(steps):
    gpio.output(stepGpio, gpio.HIGH)
    sleep(speed)
    gpio.output(stepGpio, gpio.LOW)
    sleep(speed)
