from ctypes import Structure, Union, c_char, sizeof
import serial
import time

class DataStruct(Structure):
    def __init__(self, fields):
        _fields_ = fields

class Data(Union):
    def __init__(self, fields):
        _fields_ = [('sensorData', DataStruct(fields)),
                    ('myData',     sizeof(DataStruct(fields)))]

class Serial:
    def __init__(self, data_queue, struct_fields, port='/dev/ttyACM0', baudrate=19200, timeout=1):
        self.serial_device = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.PACKET_SIZE = 6
        self.BEGIN_PAD = [0x41, 0x42]
        self.data = Data(struct_fields)
        self.serial_queue = data_queue
        self.sync()

    def write(self, data):
        self.serial_device.write(data)

    def read(self):
        while True:
            self.data.myData = serial_device.read(PACKET_SIZE)
            self.serial_queue.put(self.data.sensorData)
            time.sleep(.1)

    def readline(self):
        return self.serial_queue.get()

    def sync(self):
        while True:
            if self.serial_device.read(1) == self.BEGIN_PAD[0] \
               and self.serial_device.read(1) == self.BEGIN_PAD[1]:
               break 
        self.serial_device.read(self.PACKET_SIZE-len(self.BEGIN_PAD))
