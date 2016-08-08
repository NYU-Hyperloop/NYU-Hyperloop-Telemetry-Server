from ctypes import c_int, c_float
import ConfigParser
import serial_device as serial

type_dict = {'int': c_int, 'float': c_float}

class ServerConfig(ConfigParser.RawConfigParser, object):
    def __init__(self, config_filename):
        super(ServerConfig, self).__init__()
        self.struct_fields = []
        self.read(config_filename)
        
        assert self.has_option('Flask', 'SECRET_KEY')
        assert self.has_option('SocketIO', 'host')
        assert self.has_option('SocketIO', 'port')
        assert self.has_option('SocketIO', 'certfile')
        assert self.has_option('SocketIO', 'keyfile')
        assert self.has_option('SocketIO', 'ca_certs')
        assert self.has_option('Serial', 'port')
        assert self.has_option('Serial', 'baudrate')
        assert self.has_option('Serial', 'timeout')
        assert self.has_section('Sensors')

        for i,j in self.items('Sensors'):
            self.struct_fields.append((i,type_dict[j]))

        self.host = self.get('SocketIO', 'host')
        self.port = int(self.get('SocketIO', 'port'))
        self.certfile = self.get('SocketIO', 'certfile')
        self.keyfile = self.get('SocketIO', 'keyfile')
        self.ca_certs = self.get('SocketIO', 'ca_certs')


    def Serial(self, data_queue):
        return serial.Serial(data_queue, self.struct_fields, \
                             self.get('Serial', 'port'), \
                             int(self.get('Serial', 'baudrate')), \
                             int(self.get('Serial', 'timeout')))
