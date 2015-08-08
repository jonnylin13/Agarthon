__author__ = 'jono'

from struct import pack, unpack

class packet:

    def __init__(self):
        print('Packet has been instantiated')

    def write_string(self, data):
        # Changes string char to unicode
        chars = [ord(char) for char in data]



