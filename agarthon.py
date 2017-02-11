#! python3
# Agarthon
# Main class

__author__ = 'jono'

import requests, random, client, constants

class Agarthon:


    def __init__ (self):

        print('Starting Agarthon...')

        self.info = self.get_info()
        self.regions = self.get_regions()
        self.server_info = self.get_server_info()

        self.clients = {}

        # Add a client for now
        self.add_client()

    def add_client(self):
        # Starts a client - change this in the future
        client_id = len(self.clients.keys())
        c = client.Client(self, client_id)
        c.start()
        self.clients[c] = c

    def remove_client(self, id):
        self.clients[id].stop()
        del(self.client[id])

    def get_info(self):
        r = None
        info = None
        try:
            r = requests.get(constants.url + '/info')
            info = r.json()
        except Exception as ex:
            print('Could not fetch info: ' + str(ex))
        print('Fetched info...')
        return info

    # Returns the server information ip:port\nauth_key
    def get_server_info(self):
        r = None
        try:
            data_str = '{0}{2}{3}'.format(self.get_best_region(), '\n', constants.game_version)
            print('Posting with data_str: \n' + data_str)
            r = requests.post(constants.url, data=data_str)
            print('Fetched server info: ' + r.text)
        except Exception as ex:
            print('Could not fetch server info: ' + str(ex))
        return r.text.split('\n')

    # Returns all game server regions
    def get_regions(self):
        return list(self.info['regions'])

    # OK for now
    def get_best_region(self):
        r = None
        try:
            r = requests.get(constants.url.replace('m', 'gc'))
            user_region = r.text.split(' ')
            
            for region in self.regions:
                if user_region[0].split('-')[0] in region:
                    print('Using region ' + region + '...')
                    return region
        except Exception as ex:
            print('Could not determine best region: ' + str(ex))
        rand_region = random.choice(self.regions)
        print('Using region ' + rand_region + '...')
        return rand_region

    # Set input for gamemode here
    def get_gamemode(self):
        # For now just ffa
        return constants.gamemodes[0]

