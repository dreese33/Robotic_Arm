# Motor abstraction class for stepper motors without multithreading
class Motor(object):
    
    """
    Attributes:
        step_gpio: Gpio pin for step
        direction_gpio: Gpio pin for direction
        identifier: String to identify the Motor
        run: Boolean to determine whether to run the motor
        speed: Speed to run the motor at in Steps/sec
        time_until_run: Time until motor should run again
        direction: Direction to spin motor
        output: LOW = 0, HIGH = 1
    """
    # Initializer
    def __init__(self, step_gpio, direction_gpio, identifier):
        self.step_gpio = step_gpio
        self.direction_gpio = direction_gpio
        self.identifier = identifier
        self.speed = 0.0
        self.time_until_run = 0
        self.direction = 1
        self.output = 0
    
    # Reverse motor direction
    def reverse_direction(self):
        if self.direction == 0:
            self.direction = 1
        else:
            self.direction = 0
            
    def step_motor(self):
        pass

