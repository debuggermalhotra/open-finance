from wrapper import *
import numpy as np
from numpy_ringbuffer import RingBuffer
from time import sleep

while True:
    print(get_ask_prices('AAPL'))