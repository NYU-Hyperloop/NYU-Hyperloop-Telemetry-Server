from ctypes import Structure, c_int, c_uint32, c_byte, c_int32
import datetime
import logging
import random
import time

class FakeDataStruct(Structure):
    _fields_ = [('status', c_byte),
                    ('acceleration', c_int32),
                    ('velocity', c_int32),
                    ('rpm', c_int),
                    ('position', c_int),
                    ('battery_temperature', c_int32),
                    ('temp1', c_int32),
                    ('temp2', c_int32),
                    ('battery_voltage', c_int32),
                    ('battery_current', c_int32),
                    ('stripe_count', c_uint32),
                    ('time', c_int),
                    ('pneumatics', c_uint32),
                    ]

# Very raw implementation of a fake serial
class Serial:
    def __init__(self, log,  port='COM1', baudrate = 19200, timeout=1):
        self.name = "Fake Arduino"
        self.last_reading = None
        self.data_struct = FakeDataStruct()

        self.lgr = logging.getLogger(str(datetime.datetime.now()))
        print(log)
        fhr = logging.FileHandler(log)
        fhr.setFormatter(logging.Formatter('%(message)s'))
        self.lgr.addHandler(fhr)
        self.lgr.setLevel(logging.INFO)

    def write(self, string):
        print("SEND TO ARDUINO:", string)
        print('\n')

    def read(self):
        while True:
            self.data_struct.status = random.randint(0,5);
            self.data_struct.acceleration = random.randint(-50,50)
            self.data_struct.velocity = random.randint(0,150)
            self.data_struct.rpm = random.randint(0,5603)
            self.data_struct.position = random.randint(0,5500)
            self.data_struct.temp1 = random.randint(0,150)
            self.data_struct.temp2 = random.randint(0,150)
            self.data_struct.battery_voltage = random.randint(0,16)
            self.data_struct.battery_current = random.randint(0,10)
            self.data_struct.battery_temperature = random.randint(0,150)
            self.data_struct.stripe_count = random.randint(0,50)
            self.data_struct.time = random.randint(0,65)
            self.data_struct.pneumatics = random.randint(0,4096)

            self.last_reading = self.serialize()
            self.lgr.info(self.last_reading)
            time.sleep(.1)

    def readline(self):
        return self.last_reading

    def serialize(self):
        return dict((field, getattr(self.data_struct, field)) \
            for field, _ in self.data_struct._fields_ if (field != 'begin_pad'))
