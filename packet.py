__author__ = 'jono'

import struct

class Packet:

    # Little Endian uses prefix <B

    def __init__(self, input=bytearray(), output=bytearray()):
        self.input = input
        self.output = output

    # write null terminated utf-16 string
    def write_string(self, data):
        self.output += struct.pack('<B%iB' % (len(data)-1), *map(ord, data))

    # Use to send opcodes too - write byte
    def write_uint8(self, data):
        self.output += struct.pack('<B', data)

    # write short
    def write_uint16(self, data):
        self.output += struct.pack('<h', data)

    # write int
    def write_uint32(self, data):
        self.output += struct.pack('<I', data)

    # write float
    def write_float32(self, data):
        self.output += struct.pack('<f', data)

    # write double
    def write_float64(self, data):
        self.output += struct.pack('<q', data)

    # write boolean uint8
    def write_bool(self, data):
        if data:
            self.output += struct.pack('<B', 1)
        else:
            self.output += struct.pack('<B', 0)

    # return byte - unsigned 1 byte integer
    def read_uint8(self):
        value, = struct.unpack('<B', self.input[:1])
        self.input = self.input[1:]
        return value

    # return short - unsigned 2 byte integer
    def read_uint16(self):
        value, = struct.unpack('<h', self.input[:2])
        self.input = self.input[2:]
        return value

    # return int - unsigned 4 byte integer
    def read_uint32(self):
        value, = struct.unpack('<I', self.input[:4])
        self.input = self.input[4:]
        return value

    # return float - signed 4 byte floating point value
    def read_float32(self):
        value, = struct.unpack('<f', self.input[:4])
        self.input = self.input[4:]
        return value

    # return double - signed 8 byte floating point value
    def read_float64(self):
        value, = struct.unpack('<q', self.input[:8])
        self.input = self.input[8:]
        return value

    # return boolean (uint8)
    def read_bool(self):
        value, = struct.unpack('<B', self.input[:1])
        self.input = self.input[1:]
        return value

    def read_str8(self):
        string_arr = []
        while True:
            bytes = self.read_uint8()
            if len(bytes) == 0: break
            string_arr.append(chr(bytes))
        return ''.join(string_arr)

    def read_str16(self):
        string_arr = []
        while True:
            bytes = self.read_uint16()
            if len(bytes) == 0: break
            string_arr.append(chr(bytes))
        return ''.join(string_arr)

    def skip(self, size):
        self.input = self.input[size:]

    def read_session(self, session):
        self.input = session.read()

    def clear_input(self):
        self.input = []

    def flush_session(self, session):
        session.send(self.output)
        self.output = []



