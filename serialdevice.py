from ctypes import c_byte
import serial
import time

class Serial:
    def __init__(self, data_queue, data, port='/dev/ttyACM0', baudrate=19200, timeout=1):
        self.serial_device = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.PACKET_SIZE = data.packet_size
        self.BEGIN_PAD = data.begin_pad
        self.data = data.data
        self.serial_queue = data_queue
        self.sync()

    def write(self, data):
        self.serial_device.write(data)

    def read(self):
        while True:
            tmp = self.serial_device.read(self.PACKET_SIZE)
            self.data.data_buffer = (c_byte * self.PACKET_SIZE).from_buffer_copy(tmp)
            if self.packet_verified():
                self.serialize_and_put()
            time.sleep(.2)

    def readline(self):
        return self.serial_queue.get()

    def sync(self):
        bytes_read = []
        while True:
            b = self.serial_device.read(1)
            if b == self.BEGIN_PAD[len(bytes_read)]:
                bytes_read.append(b)
                if len(bytes_read) == len(self.BEGIN_PAD):
                    break

        self.serial_device.read(self.PACKET_SIZE-len(self.BEGIN_PAD))

    def packet_verified(self):
        for i, _ in enumerate(self.BEGIN_PAD):
            if ord(self.BEGIN_PAD[i]) != self.data.sensor_data.begin_pad[i]:
                return False

        return True

    def serialize_and_put(self):
        self.serial_queue.put(dict((field, getattr(self.data.sensor_data, field)) \
            for field, _ in self.data.sensor_data._fields_ if (field != 'begin_pad')))
