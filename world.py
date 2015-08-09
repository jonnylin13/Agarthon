__author__ = 'jono'

class World:

    def __init__(self):
        print('World instantiated')
        self.player_blobs = []

    def update(self, eats, blobs, removals):
        print('Updated')

    def update_player_blobs(self, blob_id):
        if blob_id not in self.player_blobs:
            self.player_blobs.append(blob_id)

    def update_player_exp(self, level, current_xp, next_xp):
        print()

    def stop(self):
        print()

