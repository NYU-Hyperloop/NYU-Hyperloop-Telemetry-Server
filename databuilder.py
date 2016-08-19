from ctypes import Structure, Union, c_byte, c_int, c_float, sizeof

TYPE_DICT = {'int': c_int, 'float': c_float}

class DataStruct(Structure):
    pass

class Data(Union):
    pass

class DataBuilder:
    def __init__(self, begin_pad_config, sensors):
        self.begin_pad = [bytes(chr(int(i,16))) for i in begin_pad_config.split(',')]
        self.construct_fields(sensors)

        DataStruct._fields_ = self.struct_fields

        Data._fields_ = [('sensor_data', DataStruct),
                         ('data_buffer',     c_byte * self.packet_size)]

        self.data = Data()
        self.data.sensor_data = DataStruct()

    def construct_fields(self, sensors):
        self.struct_fields = [('begin_pad', c_byte * len(self.begin_pad))]
        self.packet_size = len(self.begin_pad)
        for i,(_sensor, _type) in enumerate(sensors):
            assert(_type in TYPE_DICT.keys())
            self.struct_fields.append((_sensor, TYPE_DICT[_type]))
            self.packet_size += 4
