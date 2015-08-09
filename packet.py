__author__ = 'jono'

from struct import pack, unpack

class packet:

    # Little Endian uses prefix <B

    def __init__(self, input=bytearray(), output=bytearray()):
        print('Packet has been instantiated')
        self.input = input
        self.output = output

    def write_string(self, data):
        # Changes string char to unicode
        chars = [ord(char) for char in data]
        self.output += pack('<B ' + str(len(data)) + 'H', 0, *chars)

    def read_session(self, session):
        self.input = session.read()

    def flush_session(self, session):
        session.send(self.output)
        self.output = []



