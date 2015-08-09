__author__ = 'jono'

import session, world

# Needed for game_version reconnect opcode 255
game_version = 154669603
protocol_version = 5

c2s_opcodes = {'protocol_handshake':254, 'game_version_handshake':255, 'token':80,
               'set_nickname':0, 'spectate':1, 'mouse_move':16, 'split':17, 'q_pressed':18,
               'q_released':19, 'eject_mass':21}
s2c_opcodes = {16:'world_update'}


class client:

    def __init__(self, agarthon):
        self.main = agarthon
        self.session = session.session(self.main)
        self.session.start()
        self.world = world.world()

    def is_connected(self):
        return self.is_connected()

    def start(self):
        self.send_handshake()

    def parse_packets(self):
        for packet in self.session.data_in:
            # Loads one packet into packet.input
            self.packet.read_session(self.session)

            opcode = self.packet.read_uint8()
            if s2c_opcodes[opcode] == 'world_update':
                self.world_update()

            # Clears packet.input for the next iteration
            self.packet.clear_input()

    def world_update(self):
        print('World update called!')
        count_eats = self.main.packet.read_uint16()

    # Specifically passes socket arg because must send connection token immediately after connection?
    def send_handshake(self):
        try:

            # send protocol version
            self.main.packet.write_uint8(c2s_opcodes['protocol_handshake'])
            self.main.packet.write_uint32(protocol_version)
            self.main.packet.flush_session(self.session)

            # send game version
            self.main.packet.write_uint8(c2s_opcodes['game_version_handshake'])
            self.main.packet.write_uint32(game_version)
            self.main.packet.flush_session(self.session)

            # send connection token
            self.main.packet.write_uint8(c2s_opcodes['token'])
            self.main.packet.write_string(self.session.token)
            self.main.packet.flush_session(self.session)

            print('Connection token sent!')
        except Exception as ex:
            print('Could not send connection token for reason: ' + str(ex))

    def send_set_nickname(self, name):
        try:
            self.main.packet.write_uint8(c2s_opcodes['set_nickname'])
            self.main.packet.write_string(name)
            self.main.packet.flush_session(self.session)
        except Exception as ex:
            print('Could not send set_nickname for reason: ' + str(ex))

    def send_spectate(self):
        try:
            self.main.packet.write_uint8(c2s_opcodes['spectate'])
            self.main.packet.flush_session(self.session)
        except Exception as ex:
            print('Could not send spectate for reason: ' + str(ex))

    def send_mouse_move(self, mouse_x, mouse_y, node_id):
        try:
            self.main.packet.write_uint8(c2s_opcodes['mouse_move'])
            self.main.packet.write_float64(mouse_x)
            self.main.packet.write_float64(mouse_y)
            self.main.packet.write_uint32(node_id)
            self.main.packet.flush_session(self.session)
        except Exception as ex:
            print('Could not send mouse_move for reason: ' + str(ex))

    def send_split(self):
        try:
            self.main.packet.write_uint8(c2s_opcodes['split'])
            self.main.packet.flush_session(self.session)
        except Exception as ex:
            print('Could not send send_split for reason: ' + str(ex))

    def send_q_pressed(self):
        try:
            self.main.packet.write_uint8(c2s_opcodes['q_pressed'])
            self.main.packet.flush_session(self.session)
        except Exception as ex:
            print('Could not send q_pressed for reason: ' + str(ex))

    def send_q_released(self):
        try:
            self.main.packet.write_uint8(c2s_opcodes['q_released'])
            self.main.packet.flush_session(self.session)
        except Exception as ex:
            print('Could not send q_released for reason: ' + str(ex))

    def send_eject_mass(self):
        try:
            self.main.packet.write_uint8(c2s_opcodes['eject_mass'])
            self.main.packet.flush_session(self.session)
        except Exception as ex:
            print('Could not send eject_mass for reason: ' + str(ex))

