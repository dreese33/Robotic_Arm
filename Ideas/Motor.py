#Motor abstraction class for stepper motors without multithreading
class Motor(object):
    
    """
    Attributes:
        stepGpio: Gpio pin for step
        directionGpio: Gpio pin for direction
        identifier: String to identify the Motor
        run: Boolean to determine whether to run the motor
        speed: Speed to run the motor at in Steps/sec
        timeUntilRun: Time until motor should run again
        direction: Direction to spin motor
        output: LOW = 0, HIGH = 1
    """
    #Initializer
    def _init_(self, stepGpio, directionGpio, identifier):
        self.stepGpio = stepGpio
        self.directionGpio = directionGpio
        self.identifier = identifier
        self.speed = 0.0
        self.timeUntilRun = 0
        self.direction = 1
        self.output = 0
    
    #Reverse motor direction
    def reverseDirection():
        if (self.direction == 0):
            self.direction = 1
        else:
            self.direction = 0
            
    def stepMotor():
        pass
        