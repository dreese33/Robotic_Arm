# Repeated timer code using multithreading
from threading import Timer


class RepeatedTimer(object):
    def __init__(self, interval, function):
        self.timer = None
        self.interval = interval
        self.function = function
        self.isRunning = False
        self.start()

    def _run(self):
        self.isRunning = False
        self.start()
        self.function()

    # Recursively starts new timers, so there is a slight delay between timers being started,
    # something in the milliseconds (in between steps)
    def start(self):
        if not self.isRunning:
            self.timer = Timer(self.interval, self._run)
            self.timer.start()
            self.isRunning = True

    def stop(self):
        self.timer.cancel()
        self.isRunning = False
