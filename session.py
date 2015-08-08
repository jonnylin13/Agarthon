__author__ = 'jono'

import websocket

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

    # Specifically passes socket arg because must send connection token immediately after connection?
    def send_connection_token(self, socket):
        # token_pack = bytes(self.token, 'utf-8')
        try:
            # socket.send(token_pack, 80)
            print('Connection token sent!')
        except Exception as ex:
            print('Could not send connection token for reason: ' + str(ex))