import ConfigParser
import databuilder
import fakeserial
import serialdevice

class ServerConfig(ConfigParser.RawConfigParser, object):
    def __init__(self, config_filename, testing):
        super(ServerConfig, self).__init__()
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
        assert self.has_option('Logging', 'file')
        assert self.has_option('Logging', 'sensors')
        assert self.has_option('Auth', 'username')
        assert self.has_option('Auth', 'password')

        self.data = databuilder.DataBuilder(self.get('Sensors', 'begin_pad'), self.get_sensors())

        self.secret_key = self.get('Flask', 'SECRET_KEY')
        self.host = self.get('SocketIO', 'host')
        self.port = int(self.get('SocketIO', 'port'))
        self.certfile = self.get('SocketIO', 'certfile')
        self.keyfile = self.get('SocketIO', 'keyfile')
        self.ca_certs = self.get('SocketIO', 'ca_certs')

        self.username = self.get('Auth', 'username')
        self.password = self.get('Auth', 'password')

        self.log = self.get('Logging', 'file')

        self.authorized_ips = self.get_authorized_ips()
        
        self.logged_sensors = self.get_logged_sensors()

    def Serial(self):
        if self.testing:
            return fakeserial.Serial(self.log)
        else:
            return serialdevice.Serial(self.data, \
                                       self.log, \
                                       self.get('Serial', 'port'), \
                                       int(self.get('Serial', 'baudrate')), \
                                       int(self.get('Serial', 'timeout')))

    def get_sensors(self):
        return [(i,j) for i,j in self.items('Sensors') if i != 'begin_pad']

    def get_logged_sensors(self):
        return [j for i,j in self.items('Logging') if 'sensor_' in i]

    def get_authorized_ips(self):
        return [j for i,j in self.items('AuthorizedIPs') if 'ip_' in i]
