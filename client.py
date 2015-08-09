__author__ = 'jono'

import session, world, gameview
# Needed for game_version reconnect opcode 255
game_version = 154669603
protocol_version = 5

c2s_opcodes = {'protocol_handshake':254, 'game_version_handshake':255, 'token':80,
               'set_nickname':0, 'spectate':1, 'mouse_move':16, 'split':17, 'q_pressed':18,
               'q_released':19, 'eject_mass':21}
s2c_opcodes = {16:'world_update', 17:'view_update', 20:'reset', 21:'draw_debug_line', 32:'owns_blob',
               'ffa_leaderboard':49}


class Client:

    def __init__(self, agarthon):
        self.main = agarthon
        self.session = session.Session(self.main)
        self.session.start()
        self.world = world.World()
        self.gameview = gameview.GameView()

    def is_connected(self):
        return self.is_connected()

    def start(self):
        self.send_handshake()

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

            # Clears packet.input for the next iteration
            self.packet.clear_input()

    def world_update(self):
        count_eats = self.main.packet.read_uint16()
        # Dictionary stores by key=eater_id value=victim_id THESE ARE BLOB EVENTS
        eats = {}
        for x in range(0, count_eats):
            eater_id = self.main.packet.read_uint32()
            victim_id = self.main.packet.read_uint32()
            eats[eater_id] = victim_id
        # blobs is a dict with key=player_id and value=a tuple with player information
        blobs = {}
        # Next block is sent until player id is 0
        while True:
            player_id = self.main.packet.read_uint32()
            if player_id == 0:
                break
            x = self.main.packet.read_uint32()
            y = self.main.packet.read_uint32()
            size = self.main.packet.read_uint16()
            r = self.main.packet.read_uint16()
            g = self.main.packet.read_uint16()
            b = self.main.packet.read_uint16()
            byte = self.main.packet.read_uint8()
            is_virus = byte & 0
            # Assuming this is for agitated viruses?
            is_agitated = byte & 4
            if byte & 1:
                self.main.packet.skip(4)
            elif byte & 2:
                # Blob has a skin - just skip
                skin_uri = self.main.packet.read_str8()
            name = self.main.packet.read_str16()
            blobs[player_id] = (x, y, size, r, g, b, is_virus, is_agitated, skin_uri, name)
        # Loop amt of removals, store in list of player_ids to remove
        count_removals = self.main.packet.read_uint32()
        removals = []
        for x in range(0, count_removals):
            removals.append(self.main.packet.read_uint32())
        self.world.update(eats, blobs, removals)

    def view_update(self):
        view_x = self.main.packet.read_float32()
        view_y = self.main.packet.read_float32()
        view_zoom = self.main.packet.read_float32()
        self.gameview.update(view_x, view_y, view_zoom)

    def reset(self):
        # Does nothing for now I guess
        print('Reset sent from server to client!')

    def draw_debug_line(self):
        line_x = self.main.packet.read_uint16
        liny_y = self.main.packet.read_uint16
        self.gameview.draw_debug_line()

    # Sent when respawned or split - updates the player's blobs
    def owns_blob(self):
        blob_id = self.main.packet.read_uint32()
        self.world.update_player_blobs(blob_id)

    def ffa_leaderboard(self):
        count = self.main.packet.read_uint32()
        blobs = {}
        for x in range(0, count):
            blob_id = self.main.packet.read_uint32()
            name = self.main.packet.read_str16()
            blobs[blob_id] = name
        self.gameview.update_ffa_leaderboard(blobs)

    # Sent when joining a server world

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

