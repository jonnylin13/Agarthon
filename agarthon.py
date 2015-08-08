__author__ = 'jono'

import requests, random, websocket
from struct import pack, unpack

url = 'http://m.agar.io'
# version number no longer needed?
version_number = '154669603'
gamemodes = ('ffa', 'party', 'experimental', 'teams')


class main:

    def __init__ (self):

        self.regions = self.get_regions()
        self.server_info = self.get_server_info()

        self.session = session(self.server_info)

    # Connects to the server!!! Main function
    def get_server_info(self):
        r = None
        try:
            r = requests.post(url, data=self.get_best_region())
            print('Received server info: ' + r.text)
        except Exception as ex:
            print('Could not retrieve server info: ' +str(ex))
        return r.text.split('\n')

    # Returns all game server regions
    def get_regions(self):
        r = None
        info = None
        try:
            r = requests.get(url + '/info')
            info = r.json()
        except Exception as ex:
            print('Could not retrieve regions: ' + str(ex))
        return info['regions'].keys()

    # Gets best region based on string matching, not ping!
    def get_best_region(self):
        r = None
        try:
            r = requests.get(url.replace('m', 'gc'))
            user_region = r.text.split(' ')
            for region in self.regions:
                if user_region[0] in region:
                    return region
        except Exception as ex:
            print('Could not get best region: ' + str(ex))
            return random.choice(self.regions)

    # Set input for gamemode here
    def get_gamemode(self):
        # For now, hardcode
        return gamemodes[0]

class session:

    def __init__(self, server_info):

        self.is_connected = False

        self.ip = server_info[0].split(':')[0]
        self.port = server_info[0].split(':')[1]
        self.token = server_info[1]

        self.ws = self.connect()
        self.data_in = []

        # Start collecting data
        self.run()

    def connect(self):
        url = 'ws://' + self.ip + ':' + self.port + '/'
        socket = websocket.WebSocket()
        try:
            socket.connect(url=url, origin='http://agar.io')
            print('Websocket created to ' + url)
            self.send_connection_token(socket)
            self.is_connected = True
        except Exception as ex:
            print('Could not create a connection to ' + url + ' for reason: ' + str(ex))
        return socket

    def run(self):
        while self.is_connected:
            try:
                if self.ws.connected:
                    data = self.ws.recv()
                    self.data_in.append(data)
            except Exception as ex:
                print('Could not receive data from websocket connection for reason: ' + str(ex))
                break

    def disconnect(self):
        self.ws.close()
        self.is_connected = False

    def send(self):
        print('Do nothing')

    # Specifically passes socket arg because must send connection token immediately after connection
    def send_connection_token(self, socket):
        token_pack = bytes(self.token, 'utf-8')
        try:
            socket.send(token_pack, 80)
            print('Connection token sent!')
        except Exception as ex:
            print('Could not send connection token for reason: ' + str(ex))

class packet():

    def __init__(self, input=bytearray(), output=bytearray()):
        self.input = input
        self.output = output

    def




main()

