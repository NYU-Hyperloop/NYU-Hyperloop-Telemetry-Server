from ctypes import Structure, c_int, c_float
import random
import time

class FakeDataStruct(Structure):
    _fields_ = [('yaw', c_float),
                    ('pitch', c_float),
                    ('roll', c_float),
                    ('acceleration', c_float),
                    ('velocity', c_float),
                    ('rpm', c_int), 
                    ('position', c_int),
                    ('temperature_inside', c_float), 
                    ('temperature_outside', c_float), 
                    ('temperature_electronics', c_float),
                    ('eta', c_float),   
                    ]

# Very raw implementation of a fake serial
class Serial:
    def __init__(self, data_queue, port='COM1', baudrate = 19200, timeout=1):
        self.name = "Fake Arduino"
        self.serial_queue = data_queue
        self.data_struct = FakeDataStruct()

    def write(self, string):
        print("SEND TO ARDUINO:", string)

    def read(self):
        while True:
            self.data_struct.yaw = random.randint(0,400)
            self.data_struct.pitch = random.randint(0,400)
            self.data_struct.roll = random.randint(0,400)
            self.data_struct.acceleration = random.randint(0,400)
            self.data_struct.velocity = random.randint(0,400)
            self.data_struct.rpm = random.randint(0,400)
            self.data_struct.position = random.randint(0,400)
            self.data_struct.temperature_inside = random.randint(0,400)
            self.data_struct.temperature_outside = random.randint(0,400)
            self.data_struct.temperature_electronics = random.randint(0,400)
            self.data_struct.eta = random.randint(0,400)

            self.serial_queue.put(self.data_struct)
            time.sleep(.1)

    def readline(self):
        return self.serial_queue.get()
