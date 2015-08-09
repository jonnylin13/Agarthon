__author__ = 'jono'

import requests, random, packet, client

url = 'http://m.agar.io'
gamemodes = ('ffa', 'party', 'experimental', 'teams')


class Agarthon:

    def __init__ (self):

        self.regions = self.get_regions()
        self.server_info = self.get_server_info()

        self.packet = packet.Packet()

        # Starts a client - change this in the future
        self.client = client.Client(self)
        self.client.start()

    # Returns the server information ip:port\nauth_key
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

    # Hacky method of getting region, this absolutely needs to be changed!
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
        # For now just ffa
        return gamemodes[0]

