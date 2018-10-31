import pygame
from pygame.locals import *

from lib.entity.game_object import GameObject
from lib.component.map_component import *

from settings import WindowSize


class Map(GameObject):
    def __init__(self, map_id, map_client, network_client, *components):
        super().__init__(*components)
        self.map_client = map_client
        self.network_client = network_client

        self.map_id = map_id

        self.unit_has_blitted = []
        self.surface = pygame.Surface(WindowSize)
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

        self.target = (0, 0)

    def load(self):
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

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.blit(self.surface, (0, 0), self.window)


def map_factory(map_id, map_client, network_client):
    _map = Map(map_id, map_client, network_client)
    _map.add_component(MapMouseComponent())
    _map.add_component(MapReceiveComponent())
    return _map