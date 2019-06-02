from time import sleep
import RPi.GPIO as gpio
import StepperMotor
#import StepperMotorControl as stepper
#import StepperMotor as stepper

#Pin definitions
directionLarge = 20  #CW+
stepLarge = 21      #CLK+
directionSmall = 12  #CW+
stepSmall = 16       #CLK+
CW = 1    #clockwise
CCW = 0   #counter clockwise

largeStepperMoves = 0

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

"""
gpio.setup(directionLarge, gpio.OUT)
gpio.setup(stepLarge, gpio.OUT)
gpio.setup(directionSmall, gpio.OUT)
gpio.setup(stepSmall, gpio.OUT)

gpio.output(directionLarge, CW)
gpio.output(directionSmall, CW)"""

try:
    print("Hi")
    motor1 = StepperMotor.StepperMotorMultithreading(stepLarge, directionLarge, "Large")
    motor2 = StepperMotor.StepperMotorMultithreading(stepSmall, directionSmall, "Small")
    
    motor1.startMotor(240)
    motor2.startMotor(60)
    
    #while True:
       # if (motor1.stepsTaken == 200):
         #   motor1.reverseDirection()
          #  break
    
    #Do not delete this commented code yet, this is the basis for the motor scheduler library which is much more plausible than using multithreading
    #This is due to raspberry pi not being powerful enough to handle multiple threads
    #This code runs two motors simultaneously (small motor and large motor) by basing the second motors speed on the first motors speed
    """
    while True:
        #sleep(1)
        #gpio.output(directionLarge, CW)
        #gpio.output(directionSmall, CW)
        #for x in range(200):
        gpio.output(stepLarge, gpio.HIGH)
            
        if (largeStepperMoves == 5):
            gpio.output(stepSmall, gpio.HIGH)  
        sleep(0.001)
        gpio.output(stepLarge, gpio.LOW)
        
        if (largeStepperMoves == 5):
            gpio.output(stepSmall, gpio.LOW)
            largeStepperMoves = 0
        sleep(0.001)
        largeStepperMoves += 1
        largeStepperMoves = 0
        sleep(1)
        gpio.output(directionLarge, CCW)
        gpio.output(directionSmall, CCW)
        for x in range(200):
            gpio.output(stepLarge, gpio.HIGH)
            
            if (largeStepperMoves == 4):
               gpio.output(stepSmall, gpio.HIGH) 
            sleep(0.001)
            gpio.output(stepLarge, gpio.LOW)
            
            if (largeStepperMoves == 4):
                gpio.output(stepSmall, gpio.LOW)
                largeStepperMoves = 0
            sleep(0.001)
            largeStepperMoves += 1
        largeStepperMoves = 0"""

except KeyboardInterrupt:
    #Ctrl + C pressed
    print("Cleaning up, keyboard interrupt")
    gpio.cleanup()