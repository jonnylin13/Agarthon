__author__ = 'jono'

import blob


class World:

    def __init__(self):

        # Stores all blobs
        self.blobs = {}
        # Stores the ids of blobs that the player owns
        self.player_blobs = []
        self.exp = []

    def update(self, eats, blobs, removals):
        for blob_id in blobs.keys():
            self.update_blob(blob_id, blobs[blob_id])
        # Handle removals
        for blob_id in removals:
            self.delete_blob(blob_id)

    # Blob info follows format (x, y, size, r, g, b, is_virus, is_agitated, skin_uri, name)
    def update_blob(self, id, blob_info):
        if id in self.blobs.keys():
            self.blobs[id].update(blob_info)
            return
        else:
            # Create a blob object and throw it in the dict if there is none
            blob_obj = blob.Blob(id=id, x=blob_info[0], y=blob_info[1], size=blob_info[2], red=blob_info[3], green=blob_info[4],
                             blue=blob_info[5], is_virus=blob_info[6], is_agitated=blob_info[7], skin_uri=blob_info[8], name=blob_info[9])
            self.blobs[id] = blob_obj

    def delete_blob(self, id):
        if id in self.blobs.keys():
            del(self.blobs[id])

    def update_player_blobs(self, blob_id):
        if blob_id not in self.player_blobs:
            self.player_blobs.append(blob_id)

    def update_player_exp(self, level, current_xp, next_xp):
        self.exp = (level, current_xp, next_xp)

    def stop(self):
        print()

