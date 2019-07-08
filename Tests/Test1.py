from time import sleep
import RPi.GPIO as gpio


class Test1:
    def __init__(self):
        
        # Pin definitions
        self.direction_large = 20  # CW+
        self.step_large = 21      # CLK+
        self.direction_small = 12  # CW+
        self.step_small = 16       # CLK+
        self.CW = 1    # clockwise
        self.CCW = 0   # counter clockwise
        
        # Number of delays
        self.delays = 0
        self.low_ready_large = False
        self.low_ready_small = False
        self.low_high_set = False
        self.low_high_set_prev = False

        self.low_set_large = False
        self.low_set_small = False

        self.high_low_delay = 0

        # Delay from delay increment, 0.004s and 0.003s
        self.delays_small = 1
        self.delays_large = 5

        # Delay increment
        self.delay_increment = 0.001

        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)

        gpio.setup(self.direction_large, gpio.OUT)
        gpio.setup(self.step_large, gpio.OUT)
        gpio.setup(self.direction_small, gpio.OUT)
        gpio.setup(self.step_small, gpio.OUT)

        gpio.output(self.direction_large, self.CW)
        gpio.output(self.direction_small, self.CW)

    def test(self):
        try:
            # The code commented below was a failed attempt at multithreading,
            # should have a working library by next week for controlling 4 motors simultaneously,
            # as well as a direct approach of setting motor speed rather than entering the values manually.
            """motor1 = StepperMotor.StepperMotorMultithreading(stepLarge, directionLarge, "Large")
            motor2 = StepperMotor.StepperMotorMultithreading(stepSmall, directionSmall, "Small")
            
            motor1.startMotor(240)
            motor2.startMotor(60)"""
            
            # Run two motors simultaneously at any speed
            while True:
                gpio.output(self.direction_large, self.CCW)
                gpio.output(self.direction_small, self.CCW)
                for x in range(500):
                    self.low_set_large = False
                    self.low_set_small = False
                    if self.low_ready_large:
                        gpio.output(self.step_large, gpio.LOW)
                        self.low_ready_large = False
                        self.low_set_large = True
                        
                    if self.low_ready_small:
                        gpio.output(self.step_small, gpio.LOW)
                        self.low_ready_small = False
                        self.low_set_small = True
                        
                    if self.low_high_set:
                        self.low_high_set = False
                        self.low_high_set_prev = True
                    
                    if self.delays % self.delays_large == 0 and not self.low_set_large:
                        gpio.output(self.step_large, gpio.HIGH)
                        self.low_ready_large = True
                        self.low_high_set = True
                        
                    if self.delays % self.delays_small == 0 and not self.low_set_small:
                        gpio.output(self.step_small, gpio.HIGH)
                        self.low_ready_small = True
                        self.low_high_set = True
                        
                    if self.low_high_set:
                        sleep(self.delay_increment)
                        self.delays += 1
                        self.low_high_set = False
                        
                        if self.low_high_set_prev:
                            sleep(self.delay_increment)
                            self.delays += 1
                            self.low_high_set_prev = False
                    else:
                        sleep(self.delay_increment)
                        self.delays += 1
                sleep(1)
                
                gpio.output(self.direction_large, self.CW)
                gpio.output(self.direction_small, self.CW)

                for x in range(500):
                    self.low_set_large = False
                    self.low_set_small = False
                    if self.low_ready_large:
                        gpio.output(self.step_large, gpio.LOW)
                        self.low_ready_large = False
                        self.low_set_large = True

                    if self.low_ready_small:
                        gpio.output(self.step_small, gpio.LOW)
                        self.low_ready_small = False
                        self.low_set_small = True

                    if self.low_high_set:
                        self.low_high_set = False
                        self.low_high_set_prev = True

                    if self.delays % self.delays_large == 0 and not self.low_set_large:
                        gpio.output(self.step_large, gpio.HIGH)
                        self.low_ready_large = True
                        self.low_high_set = True

                    if self.delays % self.delays_small == 0 and not self.low_set_small:
                        gpio.output(self.step_small, gpio.HIGH)
                        self.low_ready_small = True
                        self.low_high_set = True

                    if self.low_high_set:
                        sleep(self.delay_increment)
                        self.delays += 1
                        self.low_high_set = False

                        if self.low_high_set_prev:
                            sleep(self.delay_increment)
                            self.delays += 1
                            self.low_high_set_prev = False
                    else:
                        sleep(self.delay_increment)
                        self.delays += 1

                sleep(1)

        except KeyboardInterrupt:
            # Ctrl + C pressed
            print("Cleaning up, keyboard interrupt")
            gpio.cleanup()
