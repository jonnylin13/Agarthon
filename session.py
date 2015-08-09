__author__ = 'jono'

import websocket

class session:

    def __init__(self, main):

        self.main = main

        self.is_connected = False

        self.ip, self.port = self.main.server_info[0].split(':')
        self.token = self.main.server_info[1]

        self.ws = self.connect()
        # Send connection token right after connected!
        self.send_connection_token()
        self.data_in = []

        # Start collecting data
        self.run()

    def connect(self):
        url = 'ws://' + self.ip + ':' + self.port + '/'
        socket = websocket.WebSocket()
        try:
            socket.connect(url=url, origin='http://agar.io')
            print('Websocket created to ' + url)
            self.is_connected = True
            return socket
        except Exception as ex:
            print('Could not create a connection to ' + url + ' for reason: ' + str(ex))

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

    # Send already formatted data
    def send(self, data):
        if self.is_connected:
            if len(data) > 0:
                try:
                    self.ws.send(data)
                    print('Sent packet: ' + str(data))
                except Exception as ex:
                    print('Could not send data for reason: ' + str(ex))
            else:
                print('Tried to send packet with no data!')
        else:
            print('Tried to send packet with no connection!')

    def read(self):
        if self.is_connected:
            if len(self.data_in) > 0:
                return_data = self.data_in[0]
                del(self.data_in[0])
                return return_data
            else:
                print('The input byte array is empty!')
        else:
            print('Tried to read byte with no connection!')

    # Specifically passes socket arg because must send connection token immediately after connection?
    def send_connection_token(self):
        try:
            self.main.packet.write_string(self.token)
            self.main.packet.flush_session(self)
            print('Connection token sent!')
        except Exception as ex:
            print('Could not send connection token for reason: ' + str(ex))