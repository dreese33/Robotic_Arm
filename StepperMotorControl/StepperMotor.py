from time import sleep
from enum import Enum
import RPi.GPIO as gpio


class MotorStates(Enum):
    OFF = 1
    LOW = 2
    HIGH = 3


class Direction(Enum):
    CW = 0
    CCW = 1
    

class Microstepping(Enum):
    ONE = 0
    HALFA = 1
    HALFB = 2
    QUARTER = 3
    EIGHTH = 4
    SIXTEENTH = 5
    THIRTYSECOND = 6


class StepperMotor:
    
    # Delay between motor steps
    currentDelayTB6600 = [0.001, 0.0005, 0.0005, 0.00025, 0.000025, 0.0001, 0.00001]
    notSet = True
    
    """
    step_gpio: Gpio pin for step
    direction_gpio: Gpio pin for direction
    steps_taken: Total steps taken, refreshed after one second or specified time interval
    total_delays_before_interval: The total number of delays, refreshed after one second or specified time interval
    steps_fraction: Precalculated so the computer does not have to perform long division more than once
    delays_fraction: Precalculated so the computer does not have to perform long division more than once
    speed: Speed in steps per second to run the motor
    state: State the motor is currently in from MotorStates
    interval: Interval for which the motor will run until it restarts the number of delays
    CW: clockwise
    CCW: counterclockwise
    current_microstepping: The current microstepping index for the microstepping array
    direction: The current direction of the motor
    gear_ratio: The ratio of gears
    
    Microstepping efficiency storing of data:
    time - Current time value
    curr_steps - Current number of steps the motor is performing
    curr_sleep - Current amount of sleep the motor has taken before switching states
    total_steps - Current amount of steps toward the curr_steps
    """
    
    def __init__(self, step_gpio, direction_gpio, current_microstepping, direction, gear_ratio = 1):
        if StepperMotor.notSet:
            gpio.setwarnings(False)
            gpio.setmode(gpio.BCM)
            
        gpio.setup(step_gpio, gpio.OUT)
        gpio.setup(direction_gpio, gpio.OUT)
        gpio.output(direction_gpio, direction.value)
        
        self.gear_ratio = gear_ratio
        self.step_gpio = step_gpio
        self.direction_gpio = direction_gpio
        
        self.total_delays_before_interval = 0
        self.steps_taken = 0
        self.delay_fraction = 0.0
        self.steps_fraction = 0.0
        
        self.speed = 0
        self.state = MotorStates.OFF
        self.interval = 1000.0
        
        self.current_microstepping = current_microstepping
        self.time = self.get_time()
        self.curr_steps = 0
        self.curr_sleep = 0
        self.total_steps = 0
        
        self.direction = direction
        
    # Sets the motors direction
    def set_direction(self, direction):
        gpio.output(self.direction_gpio, direction.value)
        self.direction = direction
        
    # Reverses direction of motor
    def reverse_direction(self):
        sleep(0.5)
        if self.direction == Direction.CW:
            gpio.output(self.direction_gpio, Direction.CCW.value)
            self.direction = Direction.CCW
        else:
            gpio.output(self.direction_gpio, Direction.CW.value)
            self.direction = Direction.CW
        
    # Returns the default delay between steps
    def get_time(self):
        return StepperMotor.currentDelayTB6600[self.current_microstepping.value]
    
    # Returns the amount to increase steps by due to microstepping
    def get_microstepping_factor(self, microstepping):
        if microstepping.value == 0:
            return 1
        elif microstepping.value == 1 or microstepping.value == 2:
            return 2
        else:
            return 2 ** (microstepping.value - 1)
        
    # Starts motor, or simply changes its speed if it is already on
    def start(self, speed = 1):
        if speed <= 0:
            return "Cannot start motor with speed <= 0"
        
        self.speed = speed
        self.steps_fraction = 1.0 / speed
        self.delay_fraction = 1.0 / self.interval   # 1000 is the default interval
        
        if self.state != MotorStates.OFF:
            return
        else:
            self.state = MotorStates.LOW
            
    # Restarts delays after interval is complete
    def restart_delays_remaining(self):
        self.total_delays_before_interval = 0
        self.steps_taken = 0

    # This function cannot be called in the high state
    # Untested
    def stop_motor(self):
        if self.state != MotorStates.HIGH:
            self.state = MotorStates.OFF
            self.speed = 0
            self.restart_delays_remaining()
        else:
            print("Do not call stopMotor() while the motor is in the middle of a step")
    
    
    # Sets the interval in milliseconds
    def set_interval(self, interval):
        if interval > 0:
            self.interval = interval
        else:
            return "Interval <= 0"
    
    # Basic stepping functionality
    # Runs motor specific number of steps, 200 = full rotation
    def step_motor(self, steps):
        if steps < 0:
            self.reverse_direction()
            steps = -steps
        elif steps == 0:
            return "Cannot step 0 times"
        
        print("Stepping")
        total_steps = steps * self.get_microstepping_factor(self.current_microstepping) * self.gear_ratio
        print(total_steps)
        print(self.get_time())
        for i in range(int(total_steps)):
            gpio.output(self.step_gpio, gpio.HIGH)
            sleep(self.get_time())
            gpio.output(self.step_gpio, gpio.LOW)
            sleep(self.get_time())
    
    # Runs motor a certain number of degrees
    def step_motor_degrees(self, degrees):
        total_steps = (float(degrees) / 360.0) * 200
        self.step_motor(total_steps)
    
    # Runs motor for specific time interval
    # Untested
    def step_motor_time_interval(self, time_interval):
        time = self.get_time()
        while time_interval > 0:
            gpio.output(self.step_gpio, gpio.HIGH)
            sleep(time)
            gpio.output(self.step_gpio, gpio.LOW)
            sleep(time)
            time_interval -= time * 2
    
    # Runs motor for currently set time interval
    # Untested
    def step_motor_interval(self):
        time_interval = self.interval
        step_motor_time_interval(time_interval)
    
    # Run multiple motors simultaneously at the same speed, microstepping settings, number of steps
    @staticmethod
    def step_motors(motors, steps):
        motors_copy = list(motors)
        
        if len(motors_copy) != len(steps):
            return "motors and steps must be the same length"
        
        for i in range(len(motors_copy)):
            if steps[i] < 0:
                motors_copy[i].reverse_direction()
                print("Reversing")
                steps[i] = -steps[i]
            elif steps[i] == 0:
                return "Cannot step 0 times"
        
        total_steps = 0
        steps_array = []
        for i in range(len(motors_copy)):
            motor = motors_copy[i]
            steps_array.append(int(steps[i] * motor.get_microstepping_factor(motor.current_microstepping) * motor.gear_ratio))
        
        delete_elements = []
        sleep_time = motors_copy[0].get_time()
        
        while True:
            for i in range(len(motors_copy)):
                gpio.output(motors_copy[i].step_gpio, gpio.HIGH)
            sleep(sleep_time)
            
            total_steps += 1
            
            for i in range(len(motors_copy)):
                gpio.output(motors_copy[i].step_gpio, gpio.LOW)
                if steps_array[i] <= total_steps:
                    delete_elements.append(i)
            sleep(sleep_time)
            
            #print("Total steps", total_steps)
            if len(delete_elements) > 0:
                delete_elements.reverse()
                for i in delete_elements:
                    del motors_copy[i]
                    del steps_array[i]
                    print("Deleting", i)
                delete_elements = []
            
            if len(motors_copy) < 1:
                break
        print("Complete")
            
    # Run multiple motors simultaneously same degrees
    @staticmethod
    def step_motors_degrees(motors, degrees):
        if len(motors) != len(degrees):
            return "number of motors must equal number of degree values"
        
        total_steps = []
        for i in range(len(motors)):
            total_steps.append((float(degrees[i]) / 360.0) * 200)
        StepperMotor.step_motors(motors, total_steps)
    
    # Steps motors specified number of steps with different microstepping values
    # Untested
    # TODO -- Try to optimize this code by using a two dimensional array
    @staticmethod
    def step_motors_micro(motors, steps):
        motors_copy = list(motors)
        
        if len(motors) != len(steps):
            return "FAILURE -- Number of motors must equal number of steps"
        
        for i in range(len(motors_copy)):
            if steps[i] < 0:
                motors_copy[i].reverse_direction()
                print("Reversing")
                steps[i] = -steps[i]
            elif steps[i] == 0:
                return "Cannot step 0 times"

        min_sleep_val = 0.00001
        delete_elements = []
        
        for i in range(len(motors_copy)):
            motor = motors_copy[i]
            motor.curr_steps = int(steps[i] * motor.get_microstepping_factor(motor.current_microstepping) * motor.gear_ratio)
            motor.curr_sleep = 0
            motor.total_steps = 0
            if motor.state == MotorStates.OFF:
                motor.start()
        
        print("Starting")
        while True:
            sleep(min_sleep_val)
            num = 0
            for motor in motors_copy:
                motor.curr_sleep += min_sleep_val
                if motor.curr_sleep >= motor.time:
                    StepperMotor.step_motor_micro(motor, delete_elements, num)
                    num += 1
            
            if len(delete_elements) > 0:
                delete_elements.reverse()
                for motor in delete_elements:
                    print("Deleting", motor, motors_copy[motor].total_steps)
                    del motors_copy[motor]
                delete_elements = []
                
            if len(motors_copy) < 1:
                break
        print("Complete")
        
    # Step internal method for step_motors_micro
    @staticmethod
    def step_motor_micro(motor, delete_elements, num):
        if motor.state == MotorStates.LOW:
            # Put motor in HIGH state
            motor.state = MotorStates.HIGH
            gpio.output(motor.step_gpio, gpio.HIGH)
            motor.curr_sleep = 0
            if motor.total_steps >= motor.curr_steps:
                delete_elements.append(num)
        elif motor.state == MotorStates.HIGH:
            # Put motor in LOW state
            motor.state = MotorStates.LOW
            gpio.output(motor.step_gpio, gpio.LOW)
            motor.curr_sleep = 0
            motor.total_steps += 1
        
        
    # Steps motors specified number of steps, speed, and supports different microstepping values
    @staticmethod
    def step_motors_custom(motors, steps, speeds):
        pass
    
    @staticmethod
    def step_degrees_micro(motors, degrees):
        pass
    
    @staticmethod
    def step_degrees_custom(motors, degrees, speeds):
        pass
    
    # Runs multiple motors with different speeds and microstepping settings
    # Runs motors for a number of degrees
    # Untested
    def run_motors_degrees(self, motors, degrees):
        degrees_to_steps = round(degrees * (5/9))
        StepperMotor.run_motors_steps(motors, degrees_to_steps)
       
    # Runs the motors a number of steps
    # Untested
    def run_motors_steps(self, motors, steps):
        if steps == 0:
            return "Steps cannot be 0"
        
        steps *= self.get_microstepping_factor(self.current_microstepping)
        real_steps_taken = []
        
        if steps < 0:
            steps = -steps
            for motor in motors:
                gpio.output(motor.direction_gpio, Direction.CCW.value)
                motor.restart_delays_remaining()
                real_steps_taken.append(0)
        else:
            for motor in motors:
                gpio.output(motor.direction_gpio, Direction.CW.value)
                motor.restart_delays_remaining()
                real_steps_taken.append(0)
        
        loop_count = 0
        while True:
            loop_count += 1
            if len(motors) == 0:
                break
            
            motor_number = 0
            print("", real_steps_taken[motor_number])
            for motor in motors:
                if real_steps_taken[motor_number] >= steps:
                    motors.remove(motor)
                    break
                if motor.total_delays_before_interval == motor.interval:
                    print("Restartting")
                    motor.restart_delays_remaining()
                if motor.state == MotorStates.LOW:
                    if (motor.delay_fraction * motor.total_delays_before_interval) >= \
                            (motor.steps_fraction * motor.steps_taken):
                        gpio.output(motor.step_gpio, gpio.HIGH)
                        motor.state = MotorStates.HIGH
                        motor.steps_taken += 1.0
                        real_steps_taken[motor_number] += 1
                    motor.total_delays_before_interval += 1.0
                elif motor.state == MotorStates.HIGH:
                    gpio.output(motor.step_gpio, gpio.LOW)
                    motor.total_delays_before_interval += 1.0
                    motor.state = MotorStates.LOW
                motor_number += 1
                motor.total_delays_before_interval += 1
            sleep(self.get_time())
            
        for motor in motors:
            motor.restart_delays_remaining()
            
        print("", loop_count)

    # Runs the motors for a specified time interval in milliseconds
    # Untested
    def run_motors_time_interval(self, motors, time_interval):
        if time_interval <= 0:
            return
        
        for i in range(time_interval):
            for motor in motors:
                if motor.total_delays_before_interval == motor.interval:
                    motor.restart_delays_remaining()
                if motor.state == MotorStates.LOW:
                    if (motor.delay_fraction * motor.total_delays_before_interval) \
                            >= (motor.steps_fraction * motor.steps_taken):
                        gpio.output(motor.step_gpio, gpio.HIGH)
                        motor.state = MotorStates.HIGH
                        motor.steps_taken += 1.0
                    motor.total_delays_before_interval += 1.0
                elif motor.state == MotorStates.HIGH:
                    gpio.output(motor.step_gpio, gpio.LOW)
                    motor.total_delays_before_interval += 1.0
                    motor.state = MotorStates.LOW
            sleep(self.get_time())
    
    # Runs the motors for their set interval
    # Untested
    def run_motors_interval(self, motors):
        while True:
            if len(motors) == 0:
                break
            
            for motor in motors:
                if motor.total_delays_before_interval == motor.interval:
                    motors.remove(motor)
                if motor.state == MotorStates.LOW:
                    if (motor.delay_fraction * motor.total_delays_before_interval) \
                            >= (motor.steps_fraction * motor.steps_taken):
                        gpio.output(motor.step_gpio, gpio.HIGH)
                        motor.state = MotorStates.HIGH
                        motor.steps_taken += 1.0
                    motor.total_delays_before_interval += 1.0
                elif motor.state == MotorStates.HIGH:
                    gpio.output(motor.step_gpio, gpio.LOW)
                    motor.total_delays_before_interval += 1.0
                    motor.state = MotorStates.LOW
            sleep(self.get_time())
