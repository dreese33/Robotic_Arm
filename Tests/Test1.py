from time import sleep
import RPi.GPIO as gpio

class Test1():
    def __init__(self):
        
        #Pin definitions
        directionLarge = 20  #CW+
        stepLarge = 21      #CLK+
        directionSmall = 12  #CW+
        stepSmall = 16       #CLK+
        CW = 1    #clockwise
        CCW = 0   #counter clockwise
        
        #Number of delays
        delays = 0
        lowReadyLarge = False
        lowReadySmall = False
        lowHighSet = False
        lowHighSetPrev = False

        lowSetLarge = False
        lowSetSmall = False

        highLowDelay = 0

        #Delay from delay increment, 0.004s and 0.003s
        delaysSmall = 1
        delaysLarge = 5

        #Delay increment
        delayIncrement = 0.001

        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)

        gpio.setup(directionLarge, gpio.OUT)
        gpio.setup(stepLarge, gpio.OUT)
        gpio.setup(directionSmall, gpio.OUT)
        gpio.setup(stepSmall, gpio.OUT)

        gpio.output(directionLarge, CW)
        gpio.output(directionSmall, CW)

    def test(self):
        try:
            #The code commented below was a failed attempt at multithreading,
            #should have a working library by next week for controlling 4 motors simultanenously,
            #as well as a direct approach of setting motor speed rather than entering the values manually.  
            """motor1 = StepperMotor.StepperMotorMultithreading(stepLarge, directionLarge, "Large")
            motor2 = StepperMotor.StepperMotorMultithreading(stepSmall, directionSmall, "Small")
            
            motor1.startMotor(240)
            motor2.startMotor(60)"""
            
            #Run two motors simultaneously at any speed
            while True:
                gpio.output(directionLarge, CCW)
                gpio.output(directionSmall, CCW)
                for x in range(500):
                    lowSetLarge = False
                    lowSetSmall = False
                    if (lowReadyLarge):
                            gpio.output(stepLarge, gpio.LOW)
                            lowReadyLarge = False
                            lowSetLarge = True
                        
                    if (lowReadySmall):
                            gpio.output(stepSmall, gpio.LOW)
                            lowReadySmall = False
                            lowSetSmall = True
                        
                    if (lowHighSet):
                        lowHighSet = False
                        lowHighSetPrev = True
                    
                    if (delays % delaysLarge == 0 and not lowSetLarge):
                        gpio.output(stepLarge, gpio.HIGH)
                        lowReadyLarge = True
                        lowHighSet = True
                        
                    if (delays % delaysSmall == 0 and not lowSetSmall):
                        gpio.output(stepSmall, gpio.HIGH)
                        lowReadySmall = True
                        lowHighSet = True
                        
                    if (lowHighSet):
                        sleep(delayIncrement)
                        delays += 1
                        lowHighSet = False
                        
                        if (lowHighSetPrev):
                            sleep(delayIncrement)
                            delays += 1
                            lowHighSetPrev = False
                    else:
                        sleep(delayIncrement)
                        delays += 1
                sleep(1)
                
                gpio.output(directionLarge, CW)
                gpio.output(directionSmall, CW)
                
                for x in range(500):
                    lowSetLarge = False
                    lowSetSmall = False
                    if (lowReadyLarge):
                            gpio.output(stepLarge, gpio.LOW)
                            lowReadyLarge = False
                            lowSetLarge = True
                        
                    if (lowReadySmall):
                            gpio.output(stepSmall, gpio.LOW)
                            lowReadySmall = False
                            lowSetSmall = True
                        
                    if (lowHighSet):
                        lowHighSet = False
                        lowHighSetPrev = True
                    
                    if (delays % delaysLarge == 0 and not lowSetLarge):
                        gpio.output(stepLarge, gpio.HIGH)
                        lowReadyLarge = True
                        lowHighSet = True
                        
                    if (delays % delaysSmall == 0 and not lowSetSmall):
                        gpio.output(stepSmall, gpio.HIGH)
                        lowReadySmall = True
                        lowHighSet = True
                        
                    if (lowHighSet):
                        sleep(delayIncrement)
                        delays += 1
                        lowHighSet = False
                        
                        if (lowHighSetPrev):
                            sleep(delayIncrement)
                            delays += 1
                            lowHighSetPrev = False
                    else:
                        sleep(delayIncrement)
                        delays += 1
                sleep(1)

        except KeyboardInterrupt:
            #Ctrl + C pressed
            print("Cleaning up, keyboard interrupt")
            gpio.cleanup()
