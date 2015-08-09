__author__ = 'jono'

import session, world, gameview, packet
# Needed for game_version reconnect opcode 255
game_version = 154669603
protocol_version = 5

c2s_opcodes = {'protocol_handshake':254, 'game_version_handshake':255, 'token':80,
               'set_nickname':0, 'spectate':1, 'mouse_move':16, 'split':17, 'q_pressed':18,
               'q_released':19, 'eject_mass':21}
s2c_opcodes = {16:'world_update', 17:'view_update', 20:'reset', 21:'draw_debug_line', 32:'owns_blob',
               'ffa_leaderboard':49, 'game_area_size':64, 'blob_experience_info':81}


class Client:

    def __init__(self, agarthon, client_id):
        self.client_id = client_id
        self.main = agarthon
        self.packet = packet.Packet()
        self.session = session.Session(self.main)
        self.session.start()
        self.world = world.World()
        self.gameview = gameview.GameView()

    def is_connected(self):
        return self.is_connected()

    def start(self):
        self.send_handshake()
        self.gameview.start()

    def stop(self):
        self.world.stop()
        self.session.disconnect()
        self.gameview.stop()

    def parse_packets(self):
        for packet in self.session.data_in:
            print('Parsing packet: '.join(packet))
            # Loads one packet into packet.input
            self.packet.read_session(self.session)

            opcode = self.packet.read_uint8()
            if s2c_opcodes[opcode] == 'world_update':
                self.world_update()
            elif s2c_opcodes[opcode] == 'view_update':
                self.view_update()
            elif s2c_opcodes[opcode] == 'reset':
                self.reset()
            elif s2c_opcodes[opcode] == 'draw_debug_line':
                self.draw_debug_line()
            elif s2c_opcodes[opcode] == 'owns_blob':
                self.owns_blob()
            elif s2c_opcodes[opcode] == 'ffa_leaderboard':
                self.ffa_leaderboard()
            elif s2c_opcodes[opcode] == 'blob_experience_info':
                self.blob_experience_info()
            elif s2c_opcodes[opcode] == 'game_area_size':
                self.game_size()
            else:
                print('Could not handle packet with opcode: ' + str(opcode))

            # Clears packet.input for the next iteration
            self.packet.clear_input()

    def world_update(self):
        count_eats = self.packet.read_uint16()
        # Dictionary stores by key=eater_id value=victim_id THESE ARE BLOB EVENTS
        eats = {}
        for x in range(0, count_eats):
            eater_id = self.packet.read_uint32()
            victim_id = self.packet.read_uint32()
            eats[eater_id] = victim_id
        # blobs is a dict with key=player_id and value=a tuple with player information
        blobs = {}
        # Next block is sent until player id is 0
        while True:
            player_id = self.packet.read_uint32()
            if player_id == 0:
                break
            x = self.packet.read_uint32()
            y = self.packet.read_uint32()
            size = self.packet.read_uint16()
            r = self.packet.read_uint16()
            g = self.packet.read_uint16()
            b = self.packet.read_uint16()
            byte = self.packet.read_uint8()
            is_virus = byte & 0
            # Assuming this is for agitated viruses?
            is_agitated = byte & 4
            if byte & 1:
                self.packet.skip(4)
            elif byte & 2:
                # Blob has a skin - just skip
                skin_uri = self.packet.read_str8()
            name = self.packet.read_str16()
            blobs[player_id] = (x, y, size, r, g, b, is_virus, is_agitated, skin_uri, name)
        # Loop amt of removals, store in list of player_ids to remove
        count_removals = self.packet.read_uint32()
        removals = []
        for x in range(0, count_removals):
            removals.append(self.packet.read_uint32())
        self.world.update(eats, blobs, removals)

    def view_update(self):
        view_x = self.packet.read_float32()
        view_y = self.packet.read_float32()
        view_zoom = self.packet.read_float32()
        self.gameview.update(view_x, view_y, view_zoom)

    def reset(self):
        # Does nothing for now I guess
        print('Reset sent from server to client!')

    def draw_debug_line(self):
        line_x = self.packet.read_uint16
        line_y = self.packet.read_uint16
        self.gameview.draw_debug_line(line_x, line_y)

    # Sent when respawned or split - updates the player's blobs
    def owns_blob(self):
        blob_id = self.packet.read_uint32()
        self.world.update_player_blobs(blob_id)

    def ffa_leaderboard(self):
        count = self.packet.read_uint32()
        blobs = {}
        for x in range(0, count):
            blob_id = self.packet.read_uint32()
            name = self.packet.read_str16()
            blobs[blob_id] = name
        self.gameview.update_ffa_leaderboard(blobs)

    # Player EXP info
    def blob_experience_info(self):
        level = self.packet.read_uint32()
        current_xp = self.packet.read_uint32()
        next_xp = self.packet.read_uint32()
        self.world.update_player_exp(level, current_xp, next_xp)

    def game_size(self):
        min_x = self.packet.read_float64()
        min_y = self.packet.read_float64()
        max_x = self.packet.read_float64()
        max_y = self.packet.read_float64()


    # Specifically passes socket arg because must send connection token immediately after connection?
    def send_handshake(self):
        try:

            # send protocol version
            self.packet.write_uint8(c2s_opcodes['protocol_handshake'])
            self.packet.write_uint32(protocol_version)
            self.packet.flush_session(self.session)

            # send game version
            self.packet.write_uint8(c2s_opcodes['game_version_handshake'])
            self.packet.write_uint32(game_version)
            self.packet.flush_session(self.session)

            # send connection token
            self.packet.write_uint8(c2s_opcodes['token'])
            self.packet.write_string(self.session.token)
            self.packet.flush_session(self.session)

            print('Connection token sent!')
        except Exception as ex:
            print('Could not send connection token for reason: ' + str(ex))

    def send_set_nickname(self, name):
        try:
            self.packet.write_uint8(c2s_opcodes['set_nickname'])
            self.packet.write_string(name)
            self.packet.flush_session(self.session)
        except Exception as ex:
            print('Could not send set_nickname for reason: ' + str(ex))

    def send_spectate(self):
        try:
            self.packet.write_uint8(c2s_opcodes['spectate'])
            self.packet.flush_session(self.session)
        except Exception as ex:
            print('Could not send spectate for reason: ' + str(ex))

    def send_mouse_move(self, mouse_x, mouse_y, node_id):
        try:
            self.packet.write_uint8(c2s_opcodes['mouse_move'])
            self.packet.write_float64(mouse_x)
            self.packet.write_float64(mouse_y)
            self.packet.write_uint32(node_id)
            self.packet.flush_session(self.session)
        except Exception as ex:
            print('Could not send mouse_move for reason: ' + str(ex))

    def send_split(self):
        try:
            self.packet.write_uint8(c2s_opcodes['split'])
            self.packet.flush_session(self.session)
        except Exception as ex:
            print('Could not send send_split for reason: ' + str(ex))

    def send_q_pressed(self):
        try:
            self.packet.write_uint8(c2s_opcodes['q_pressed'])
            self.packet.flush_session(self.session)
        except Exception as ex:
            print('Could not send q_pressed for reason: ' + str(ex))

    def send_q_released(self):
        try:
            self.packet.write_uint8(c2s_opcodes['q_released'])
            self.packet.flush_session(self.session)
        except Exception as ex:
            print('Could not send q_released for reason: ' + str(ex))

    def send_eject_mass(self):
        try:
            self.packet.write_uint8(c2s_opcodes['eject_mass'])
            self.packet.flush_session(self.session)
        except Exception as ex:
            print('Could not send eject_mass for reason: ' + str(ex))

