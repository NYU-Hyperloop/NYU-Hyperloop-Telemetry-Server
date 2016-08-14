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
            print tmp
            self.data.myData = (c_byte * self.PACKET_SIZE).from_buffer_copy(tmp)
            #self.data.myData = (c_byte * self.PACKET_SIZE).from_buffer_copy(self.serial_device.read(self.PACKET_SIZE))
            self.serial_queue.put(self.data.sensorData)
            time.sleep(.1)

    def readline(self):
        return self.serial_queue.get()

    def sync(self):
        print "Syncing..."
        while True:
            if self.serial_device.read(1) == self.BEGIN_PAD[0] \
               and self.serial_device.read(1) == self.BEGIN_PAD[1]:
               break 
        print "Synced!"
        self.serial_device.read(self.PACKET_SIZE-len(self.BEGIN_PAD))
