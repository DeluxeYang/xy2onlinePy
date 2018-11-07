import pygame
from pygame.locals import *

from utils.mask import Mask
from lib.entity.game_object import GameObject
from lib.state.character_state import CharacterStandNormalState
from lib.component.character_component import MainCharacterComponent


class Character(GameObject):
    def __init__(self, character_id, network_client):
        super().__init__()
        self.character_id = character_id
        self.network_client = network_client

        self.screen_rect = Rect((0, 0), (0, 0))

        self.res_info = None

        self.target = None
        self.target_list = []
        self.direction = 0
        self.is_new_target = False
        self.is_running = False

        self.mask = Mask(None, None)
        self.weapon = None

        self.is_mouse_over = False

        self.load()

    def load(self):
        player_info = self.network_client.get_player(self.character_id)
        self.res_info = self.network_client.get_character(player_info["character"])
        self.x = player_info["position"][0]
        self.y = player_info["position"][1]


def character_factory(character_id, network_client):
    character = Character(character_id, network_client)
    character.init_state(CharacterStandNormalState())
    character.add_component(MainCharacterComponent())
    return character