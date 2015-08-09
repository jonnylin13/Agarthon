__author__ = 'jono'

from struct import pack, unpack

class packet:

    # Little Endian uses prefix <B

    def __init__(self, input=bytearray(), output=bytearray()):
        print('Packet has been instantiated')
        self.input = input
        self.output = output

    def write_string(self, data):
        # Changes string char to utf-16
        utf16 = data.encode(encoding='utf-16')
        self.output += utf16

    # Use to send opcodes too
    def write_byte(self, data):
        self.output += pack('<B', data)

    def write_int(self, data):
        self.output += pack('<I', data)

    def read_session(self, session):
        self.input = session.read()

    def flush_session(self, session):
        session.send(self.output)
        self.output = []



