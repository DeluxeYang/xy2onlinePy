import pygame
from pygame.locals import *

from .game_object import GameObject

from settings import WindowSize


class Map(GameObject):
    def __init__(self, _event, map_id, map_client, z):
        super().__init__(_event)
        self.map_id = map_id
        self.map_client = map_client

        self.unit_has_blitted = []
        self.surface = None
        self.window = Rect((0, 0), WindowSize)

        self.mask = {}
        self.masks_of_unit = None

        self.map_type = 0
        self.map_width = 0
        self.map_height = 0
        self.unit_width = 0
        self.unit_height = 0
        self.col = 0
        self.row = 0
        self.n = 0
        self.coordinate = None

    def load_map_info(self):
        send_data = {
            'request': "map_info",
            'map_id': self.map_id,
        }
        self.map_client.send(send_data)

    def quest(self, unit_id):
        send_data = {
            'request': "map_unit",
            'map_id': self.map_id,
            'unit_num': unit_id
        }
        self.map_client.send(send_data)

    def find_path(self, mouse_pos, is_running):
        send_data = {
            'request': "find_path",
            'map_id': self.map_id,
            'current': self.window.center,
            'target': mouse_pos,
            'is_running': is_running
        }
        self.map_client.send(send_data)

    def on_receive_map_info(self, event):
        pass

    def on_receive_map_unit(self, event):
        pass

    def on_mouse_left_down(self, event):
        pass

    def on_mouse_right_down(self, event):
        pass

