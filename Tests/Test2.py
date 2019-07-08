from time import sleep
import RPi.GPIO as gpio
from pynput.keyboard import Key, Listener

"""Pin definitions"""
direction_large = 20  # CW+
step_large = 21      # CLK+
direction_small = 12  # CW+
step_small = 16       # CLK+
CW = 1    # clockwise
CCW = 0   # counter clockwise

# Delay increment
delay_increment = 0.001

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

gpio.setup(direction_large, gpio.OUT)
gpio.setup(step_large, gpio.OUT)
gpio.setup(direction_small, gpio.OUT)
gpio.setup(step_small, gpio.OUT)

gpio.output(direction_large, CW)
gpio.output(direction_small, CW)


def on_press(key):
    print(format(key))


def run_rotation():
    """Moves both motors 200 steps"""
    for i in range(200):
        gpio.output(step_large, gpio.HIGH)
        gpio.output(step_small, gpio.HIGH)
        sleep(delay_increment)
        gpio.output(step_large, gpio.LOW)
        gpio.output(step_small, gpio.LOW)
        sleep(delay_increment)
    sleep(1)


def run_forward():
    gpio.output(direction_large, CW)
    gpio.output(direction_small, CW)
    run_rotation()


def run_back():
    gpio.output(direction_large, CCW)
    gpio.output(direction_small, CCW)
    run_rotation()


def on_release(key):
    if key == Key.esc:
        return False
    if key == Key.left:
        run_forward()
    if key == Key.right:
        run_back()


with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
