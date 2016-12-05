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
                    ('time_remaining', c_int),
                    ]

# Very raw implementation of a fake serial
class Serial:
    def __init__(self, port='COM1', baudrate = 19200, timeout=1):
        self.name = "Fake Arduino"
        self.last_reading = None
        self.data_struct = FakeDataStruct()

    def write(self, string):
        print("SEND TO ARDUINO:", string)
        print('\n')

    def read(self):
        while True:
            self.data_struct.yaw = random.uniform(0,90)
            self.data_struct.pitch = random.uniform(-45,45)
            self.data_struct.roll = random.uniform(-45,45)
            self.data_struct.acceleration = random.uniform(-50,50)
            self.data_struct.velocity = random.uniform(0,150)
            self.data_struct.rpm = random.randint(0,5603)
            self.data_struct.position = random.randint(0,5500)
            self.data_struct.temperature_inside = random.uniform(0,150)
            self.data_struct.temperature_outside = random.uniform(0,150)
            self.data_struct.temperature_electronics = random.uniform(0,150)
            self.data_struct.time_remaining = random.randint(0,65)

            self.last_reading = self.serialize()
            time.sleep(.1)

    def readline(self):
        return self.last_reading

    def serialize(self):
        return dict((field, getattr(self.data_struct, field)) \
            for field, _ in self.data_struct._fields_ if (field != 'begin_pad'))
