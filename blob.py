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

    def get_id(self):
        return self.id

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_size(self):
        return self.size

    def get_red(self):
        return self.red

    def get_green(self):
        return self.green

    def get_blue(self):
        return self.blue

    def get_is_virus(self):
        return self.is_virus

    def get_is_agitated(self):
        return self.is_agitated

    def get_uri(self):
        return self.uri()

    def get_name(self):
        return self.name

        


