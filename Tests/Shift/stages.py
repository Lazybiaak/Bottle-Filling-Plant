import random
import time

def is_bottle_available():
    return random.random() < 0.95

def fill_bottle():
    time.sleep(10)
    return