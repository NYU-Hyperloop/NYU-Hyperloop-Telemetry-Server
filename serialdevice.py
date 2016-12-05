"""serialdevice.py exposes the Serial class
for reading from and writing to the Arduino"""
from ctypes import c_byte
import datetime
import logging
import time

import serial


class Serial(object):
    """Serial is initialized with a DataBuilder,
    log filename, the serial port, baudrate, and a timeout
    in seconds"""
    def __init__(self, data, log, port='/dev/ttyACM0', baudrate=19200, timeout=1):
        self.serial_device = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.packet_size = data.packet_size
        self.begin_pad = data.begin_pad
        self.data = data.data
        self.last_reading = None

        self.lgr = logging.getLogger(datetime.datetime.now())
        fhr = logging.FileHandler(log)
        fhr.setFormatter(logging.Formatter('%(message)s'))
        self.lgr.addHandler(fhr)
        self.sync()

    def write(self, data):
        """write() writes a data
        object to the serial port"""
        self.serial_device.write(data)

    def read(self):
        while True:
            self.sync()
            tmp = self.serial_device.read(self.packet_size)
            self.data.data_buffer = (c_byte * self.packet_size).from_buffer_copy(tmp)
            self.last_reading = self.serialize()
            self.lgr()
            time.sleep(.2)

    def readline(self):
        return self.last_reading

    def sync(self):
        bytes_read = []
        while True:
            b = self.serial_device.read(1)
            if b == self.begin_pad[len(bytes_read)]:
                bytes_read.append(b)
                if len(bytes_read) == len(self.begin_pad):
                    break

    def serialize(self):
        return dict((field, getattr(self.data.sensor_data, field)) \
            for field, _ in self.data.sensor_data._fields_ if (field != 'begin_pad'))