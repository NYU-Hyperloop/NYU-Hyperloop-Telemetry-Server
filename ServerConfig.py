import ConfigParser
import DataBuilder
import fakeserial
import serial_device

class ServerConfig(ConfigParser.RawConfigParser, object):
    def __init__(self, config_filename, testing):
        super(ServerConfig, self).__init__()
        self.struct_fields = []
        self.read(config_filename)
        self.testing = testing
        
        assert self.has_option('Flask', 'SECRET_KEY')
        assert self.has_option('SocketIO', 'host')
        assert self.has_option('SocketIO', 'port')
        assert self.has_option('SocketIO', 'certfile')
        assert self.has_option('SocketIO', 'keyfile')
        assert self.has_option('SocketIO', 'ca_certs')
        assert self.has_option('Serial', 'port')
        assert self.has_option('Serial', 'baudrate')
        assert self.has_option('Serial', 'timeout')
        assert self.has_option('Sensors', 'begin_pad')

        self.data = DataBuilder.DataBuilder(self.get('Sensors', 'begin_pad'), self.get_sensors())

        self.host = self.get('SocketIO', 'host')
        self.port = int(self.get('SocketIO', 'port'))
        self.certfile = self.get('SocketIO', 'certfile')
        self.keyfile = self.get('SocketIO', 'keyfile')
        self.ca_certs = self.get('SocketIO', 'ca_certs')


    def Serial(self, data_queue):
        if self.testing:
            return fakeserial.Serial(data_queue, self.data)
        else:
            return serial_device.Serial(data_queue, self.data, \
                                       self.get('Serial', 'port'), \
                                       int(self.get('Serial', 'baudrate')), \
                                       int(self.get('Serial', 'timeout')))

    def get_sensors(self):
        return [(i,j) for i,j in self.items('Sensors') if i != 'begin_pad']
