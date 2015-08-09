__author__ = 'jono'

import struct

class packet:

    # Little Endian uses prefix <B

    def __init__(self, input=bytearray(), output=bytearray()):
        print('Packet has been instantiated')
        self.input = input
        self.output = output

    # write null terminated utf-16 string
    def write_string(self, data):
        # thank you Gjum for this piece
        self.output += struct.pack('<B%iB' % (len(data)-1), *map(ord, data))

    # Use to send opcodes too - write uint8
    def write_byte(self, data):
        self.output += struct.pack('<B', data)

    # write uint16
    def write_short(self, data):
        self.output += struct.pack('<h', data)

    # write uint32
    def write_int(self, data):
        self.output += struct.pack('<I', data)

    # write float32
    def write_float(self, data):
        self.output += struct.pack('<f', data)

    # write float64
    def write_double(self, data):
        self.output += struct.pack('<q', data)

    # write boolean uint8
    def write_bool(self, data):
        if data:
            self.output += struct.pack('<B', 1)
        else:
            self.output += struct.pack('<B', 0)

    # return uint8 - unsigned 1 byte integer
    def read_byte(self):
        value, = struct.unpack('<B', self.input[:1])
        self.input = self.input[1:]
        return value

    # return uint16 - unsigned 2 byte integer
    def read_short(self):
        value, = struct.unpack('<h', self.input[:2])
        self.input = self.input[2:]
        return value

    # return uint32 - unsigned 4 byte integer
    def read_int(self):
        value, = struct.unpack('<I', self.input[:4])
        self.input = self.input[4:]
        return value

    # return float32 - signed 4 byte floating point value
    def read_float(self):
        value, = struct.unpack('<f', self.input[:4])
        self.input = self.input[4:]
        return value

    # return float64 - signed 8 byte floating point value
    def read_double(self):
        value, = struct.unpack('<q', self.input[:8])
        self.input = self.input[8:]
        return value

    # return boolean (uint8)
    def read_bool(self):
        value, = struct.unpack('<B', self.input[:1])
        self.input = self.input[1:]
        return value

    def skip(self, size):
        self.input = self.input[size:]

    def read_session(self, session):
        self.input = session.read()

    def flush_session(self, session):
        session.send(self.output)
        self.output = []



