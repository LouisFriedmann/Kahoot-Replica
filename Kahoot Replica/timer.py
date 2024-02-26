# timer.py contains the timer to the used for the game

import time

class Timer:

    # Default constructor
    def __init__(self):
        self.start_time = 0

    # Function starts the timer
    def start(self):
        self.start_time = time.time()

    # Function returns the elapsed time of the timer
    def elapsed_time(self):
        if self.start_time != 0:
            return time.time() - self.start_time
        else:
            return 0

    # Function resets the timer
    def reset(self):
        self.start_time = 0
