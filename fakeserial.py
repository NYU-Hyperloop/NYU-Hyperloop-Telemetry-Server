import random

# Very raw implementation of a fake serial
class Serial:
    def __init__(self, port='COM1', baudrate = 19200, timeout=1):
        self.name = "Fake Arduino"

    def write(self, string):
        print("SEND TO ARDUINO:", string)

    def readline(self):
        return str(random.random())
