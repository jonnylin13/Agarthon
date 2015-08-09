__author__ = 'jono'

import websocket, threading

class Session:

    def __init__(self, agarthon):

        self.main = agarthon

        self.ip, self.port = self.main.server_info[0].split(':')
        self.token = self.main.server_info[1]
        self.data_in = []
        self.running = False

        # Receive loop starts on self.connect() call which instantiates ws
        self.ws = None

    def start(self):
        self.connect()
        # Start the read thread (receive data loop)
        self.thread = threading.Thread(name='SessionReadThread', target=self.recv_loop)
        self.thread.start()

    def is_connected(self):
        return self.running and self.ws.connected

    def connect(self):
        url = 'ws://' + self.ip + ':' + self.port + '/'
        self.ws = websocket.WebSocket()
        try:
            self.ws.connect(url=url, origin='http://agar.io')
            self.running = True
            print('Websocket created to ' + url)
        except Exception as ex:
            print('Could not create a connection to ' + url + ' for reason: ' + str(ex))

    # Constantly updates data_in byte array from packets sent to the client by the server
    def recv_loop(self):
        while self.is_connected():
            try:
                if self.ws.connected:
                    data = self.ws.recv()
                    self.data_in.append(data)
                else:
                    print('Could not receive data because there is no websocket connection!')
                    return
            except Exception as ex:
                print('Could not receive data from websocket connection for reason: ' + str(ex))
                return

    def disconnect(self):
        self.thread.stop()
        self.ws.close()
        self.running = False

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
        if self.is_connected and self.ws.connected:
            if len(self.data_in) > 0:
                return_data = self.data_in[0]
                del(self.data_in[0])
                return return_data
            else:
                print('The input byte array is empty!')
        else:
            print('Tried to read byte with no connection!')
