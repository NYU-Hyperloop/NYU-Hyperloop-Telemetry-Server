from ctypes import Structure, Union, c_uint8, c_int32, c_uint32, c_byte
import socket

TEAM_ID = 28
PACKET_SIZE = 34


class SpaceXPacket(Structure):
    _pack_ = 1
    _fields_ = [('team_id', c_byte),
                ('status', c_byte),
                ('acceleration', c_int32),
                ('position', c_int32),
                ('velocity', c_int32),
                ('battery_voltage', c_int32),
                ('battery_current', c_int32),
                ('battery_temperature', c_int32),
                ('pod_temperature', c_int32),
                ('stripe_count', c_uint32)]


    def populate(self, p_dict):
        self.team_id = TEAM_ID
        self.status = p_dict['status']
        self.acceleration = p_dict['acceleration']
        self.position = p_dict['position']
        self.velocity = p_dict['velocity']
        self.battery_voltage = p_dict['battery_voltage']
        self.battery_current = p_dict['battery_current']
        self.battery_temperature = p_dict['battery_temperature']
        #self.pod_temperature = p_dict['pod_temperature']
        self.stripe_count = p_dict['stripe_count']


class SpaceXPacketUnion(Union):
    _fields_ = [('packet', SpaceXPacket),
                ('packet_buffer', c_byte * PACKET_SIZE)]


class SpaceXSender():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.packet_buffer = SpaceXPacketUnion()
        self.packet = self.packet_buffer.packet


    def send(self, p_dict):
        self.packet.populate(p_dict)
        self.sock.sendto(self.packet_buffer, ('192.168.0.1', 3000))
