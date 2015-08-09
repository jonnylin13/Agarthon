__author__ = 'jono'

import blob

class World:

    def __init__(self):
        # Stores the last eat events
        self.eats = {}
        # Stores all blobs
        self.blobs = {}
        # Stores the ids of blobs that the player owns
        self.player_blobs = []

    def update(self, eats, blobs, removals):
        self.eats = eats
        # Follows the exact same format, so this should be fine!
        for id in blobs.keys():
            self.update(id, )

    # Blob info follows format (x, y, size, r, g, b, is_virus, is_agitated, skin_uri, name)
    def create_blob(self, id, blob_info):
        blob_obj = blob.Blob(id=id, x=blob_info[0], y=blob_info[1], size=blob_info[2], red=blob_info[3], green=blob_info[4],
                             blue=blob_info[5], is_virus=blob_info[6], is_agitated=blob_info[7], skin_uri=blob_info[8], name=blob_info[9])
        self.blobs[id] = blob_obj


    def update_player_blobs(self, blob_id):
        if blob_id not in self.player_blobs:
            self.player_blobs.append(blob_id)

    def update_player_exp(self, level, current_xp, next_xp):
        print()

    def stop(self):
        print()

