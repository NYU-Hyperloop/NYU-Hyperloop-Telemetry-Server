from ctypes import Structure, Union, c_byte, c_int, c_float, sizeof

TYPE_DICT = {'int': c_int, 'float': c_float}

class DataStruct(Structure):
    def __init__(self, fields):
        _fields_ = fields

class Data(Union):
    def __init__(self, fields):
        _fields_ = [('sensorData', DataStruct(fields)),
                    ('myData',     c_byte * sizeof(DataStruct(fields)))]

class DataBuilder:
    def __init__(self, begin_pad, sensors):
        self.begin_pad = [c_byte(int(i,16)) for i in begin_pad.split(',')]
        self.construct_fields(sensors)
        self.data = Data(self.struct_fields)
        self.packet_size = sizeof(self.data)

    def construct_fields(self, sensors):
        self.struct_fields = [('begin_pad', c_byte * len(self.begin_pad))]
        for i,(_sensor, _type) in sensors:
            self.struct_fields.append((_sensor, TYPE_DICT[_type]))
            self.struct_fields.append(('pad' + str(i), c_byte))
