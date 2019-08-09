from time import sleep
import RPi.GPIO as gpio

stepGpio = 26#21
directionGpio = 19#20
stepGpio1 = 21
directionGpio1 = 20
stepGpio2 = 21
directionGpio2 = 20
CW = 0
CCW = 1

speed = 0.0001 #0.0003
speed1 = 0.0001
speed2 = 0.0001

steps = 3200
steps1 = 3200
steps2 = 3200

steps_full = steps * 2
steps_full1 = steps1 * 2
steps_full2 = steps2 * 2

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

#1

#setup
gpio.setup(directionGpio, gpio.OUT)
gpio.setup(stepGpio, gpio.OUT)


#setup1
gpio.setup(directionGpio1, gpio.OUT)
gpio.setup(stepGpio1, gpio.OUT)


#setup2
"""
gpio.setup(directionGpio2, gpio.OUT)
gpio.setup(stepGpio2, gpio.OUT)

gpio.output(directionGpio2, CCW)
"""
sleep(0.5)
gpio.output(directionGpio, CCW)
gpio.output(directionGpio1, CW)

for i in range(steps):
    gpio.output(stepGpio, gpio.HIGH)
    gpio.output(stepGpio1, gpio.HIGH)
    sleep(speed)
    gpio.output(stepGpio, gpio.LOW)
    gpio.output(stepGpio1, gpio.LOW)
    sleep(speed)
    
sleep(1000)
gpio.output(directionGpio, CW)
gpio.output(directionGpio1, CCW)

for i in range(steps):
    gpio.output(stepGpio, gpio.HIGH)
    gpio.output(stepGpio1, gpio.HIGH)
    sleep(speed)
    gpio.output(stepGpio, gpio.LOW)
    gpio.output(stepGpio1, gpio.LOW)
    sleep(speed)
    
sleep(1000)

for a in range(6):
    sleep(0.5)
    gpio.output(directionGpio, CCW)
    gpio.output(directionGpio1, CCW)

    for i in range(steps_full):
        gpio.output(stepGpio, gpio.HIGH)
        gpio.output(stepGpio1, gpio.HIGH)
        sleep(speed)
        gpio.output(stepGpio, gpio.LOW)
        gpio.output(stepGpio1, gpio.LOW)
        sleep(speed)
        
    sleep(0.5)
    gpio.output(directionGpio, CW)
    gpio.output(directionGpio1, CW)

    for i in range(steps_full):
        gpio.output(stepGpio, gpio.HIGH)
        gpio.output(stepGpio1, gpio.HIGH)
        sleep(speed)
        gpio.output(stepGpio, gpio.LOW)
        gpio.output(stepGpio1, gpio.LOW)
        sleep(speed)
        
sleep(0.5)
gpio.output(directionGpio, CCW)
gpio.output(directionGpio1, CCW)

for i in range(steps):
    gpio.output(stepGpio, gpio.HIGH)
    gpio.output(stepGpio1, gpio.HIGH)
    sleep(speed)
    gpio.output(stepGpio, gpio.LOW)
    gpio.output(stepGpio1, gpio.LOW)
    sleep(speed)

"""
gpio.output(directionGpio, CCW)
for i in range(steps):
    gpio.output(stepGpio, gpio.HIGH)
    sleep(speed)
    gpio.output(stepGpio, gpio.LOW)
    sleep(speed)
   """ 
"""
for i in range(steps1):
    gpio.output(stepGpio1, gpio.HIGH)
    sleep(speed1)
    gpio.output(stepGpio1, gpio.LOW)
    sleep(speed1)
    
for i in range(steps2):
    gpio.output(stepGpio2, gpio.HIGH)
    sleep(speed2)
    gpio.output(stepGpio2, gpio.LOW)
    sleep(speed2)
"""
    
#2
sleep(1000)
gpio.output(directionGpio, CW)
gpio.output(directionGpio1, CW)
gpio.output(directionGpio2, CW)

for i in range(steps_full):
    gpio.output(stepGpio, gpio.HIGH)
    sleep(speed)
    gpio.output(stepGpio, gpio.LOW)
    sleep(speed)
  
"""
for i in range(steps_full1):
    gpio.output(stepGpio1, gpio.HIGH)
    sleep(speed1)
    gpio.output(stepGpio1, gpio.LOW)
    sleep(speed1)
    
for i in range(steps_full2):
    gpio.output(stepGpio2, gpio.HIGH)
    sleep(speed2)
    gpio.output(stepGpio2, gpio.LOW)
    sleep(speed2)
"""
    
#3
sleep(0.5)
gpio.output(directionGpio, CCW)
gpio.output(directionGpio1, CCW)
gpio.output(directionGpio2, CCW)

for i in range(steps):
    gpio.output(stepGpio, gpio.HIGH)
    sleep(speed)
    gpio.output(stepGpio, gpio.LOW)
    sleep(speed)
    
"""
for i in range(steps_full1):
    gpio.output(stepGpio1, gpio.HIGH)
    sleep(speed1)
    gpio.output(stepGpio1, gpio.LOW)
    sleep(speed1)
    
for i in range(steps_full2):
    gpio.output(stepGpio2, gpio.HIGH)
    sleep(speed2)
    gpio.output(stepGpio2, gpio.LOW)
    sleep(speed2)
"""
"""
#4
#sleep(0.5)
gpio.output(directionGpio, CW)
gpio.output(directionGpio1, CW)
gpio.output(directionGpio2, CW)

for i in range(steps_full):
    gpio.output(stepGpio, gpio.HIGH)
    sleep(speed)
    gpio.output(stepGpio, gpio.LOW)
    sleep(speed)
    
"""
"""
for i in range(steps_full1):
    gpio.output(stepGpio1, gpio.HIGH)
    sleep(speed1)
    gpio.output(stepGpio1, gpio.LOW)
    sleep(speed1)
    
for i in range(steps_full2):
    gpio.output(stepGpio2, gpio.HIGH)
    sleep(speed2)
    gpio.output(stepGpio2, gpio.LOW)
    sleep(speed2)
"""
"""
#5
#sleep(0.5)
gpio.output(directionGpio, CCW)
gpio.output(directionGpio1, CCW)
gpio.output(directionGpio2, CCW)

for i in range(steps):
    gpio.output(stepGpio, gpio.HIGH)
    sleep(speed)
    gpio.output(stepGpio, gpio.LOW)
    sleep(speed)
    
"""
"""
for i in range(steps1):
    gpio.output(stepGpio1, gpio.HIGH)
    sleep(speed1)
    gpio.output(stepGpio1, gpio.LOW)
    sleep(speed1)
    
for i in range(steps2):
    gpio.output(stepGpio2, gpio.HIGH)
    sleep(speed2)
    gpio.output(stepGpio2, gpio.LOW)
    sleep(speed2)
"""