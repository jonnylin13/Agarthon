__author__ = 'jono'


class Blob(object):

    def __init__(self, id, x, y, size, red, green, blue, is_virus, is_agitated, uri, name):
        self.id = id
        self.x = x
        self.y = y
        self.size = size
        self.red = red
        self.green = green
        self.blue = blue
        self.is_virus = is_virus
        self.is_agitated = is_agitated
        self.uri = uri
        self.name = name

    def update(self, blob_info):
        self.x = blob_info[0]
        self.y = blob_info[1]
        self.size = blob_info[2]
        self.red = blob_info[3]
        self.green = blob_info[4]
        self.blue = blob_info[5]
        self.is_virus = blob_info[6]
        self.is_agitated = blob_info[7]
        self.uri = blob_info[8]
        self.name = blob_info[9]

