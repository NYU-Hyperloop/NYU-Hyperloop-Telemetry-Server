from ctypes import Structure, Union, c_int, sizeof
import random
import time

class FakeDataStruct(Structure):
    def __init__(self, fields):
        _fields_ = fields

# Very raw implementation of a fake serial
class Serial:
    def __init__(self, data_queue, struct_fields, port='COM1', baudrate = 19200, timeout=1):
        self.name = "Fake Arduino"
        self.serial_queue = data_queue
        self.data_struct = FakeDataStruct(struct_fields)

    def write(self, string):
        print("SEND TO ARDUINO:", string)

    def read(self):
        while True:
            self.data_struct.testsensor = random.randint(0,65535)
            self.serial_queue.put(self.data_struct)
            time.sleep(.1)

    def readline(self):
        return self.serial_queue.get()
