__author__ = 'jono'

import pygame

caption = 'Agarthon by jonnylin13'

import threading

class GameView:

    def __init__(self):

        pygame.init()
        pygame.font.init()
        self.resolution = self.width, self.height = 800, 600
        self.display = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption(caption)

        self.scoreboard = {}
        self.view_x = 0
        self.view_y = 0
        self.view_zoom = None

        self.view_min_x = 0
        self.view_min_y = 0
        self.view_max_x = 0
        self.view_max_y = 0

        self.thread = None

    def update(self, view_x, view_y, view_zoom):
        self.view_x = view_x
        self.view_y = view_y
        self.view_zoom = view_zoom

    def start(self):
        self.game_loop()

    def game_loop(self):

        game_exit = False

        while not game_exit:

            self.display.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    self.stop()

            pygame.display.update()

    def draw_blob(self, blob):
        pygame.draw.circle(self.display, (blob.red, blob.green, blob.blue), (blob.x, blob.x), blob.size)

    def draw_debug_line(self, line_x, line_y):
        print('Debug line wants to be drawn but the function hasnt been coded yet!')

    def update_ffa_leaderboard(self, blobs):
        self.scoreboard = blobs

    def update_game_size(self, min_x, min_y, max_x, max_y):
        self.view_min_x = min_x
        self.view_min_y = min_y
        self.view_max_x = max_x
        self.view_max_y = max_y

    def stop(self):
        pygame.quit()
        quit()
        print('Stop wants to be called but the function hasnt been coded yet!')
