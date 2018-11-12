import pygame
from pygame.locals import *

from utils.mask import Mask
from core.entity.game_object import GameObject
from core.state.state import state_factory
from game.character.character_state import CharacterStandNormalState
from game.character.character_component import  MainCharacterComponent, CharacterMouseComponent


class Character(GameObject):
    def __init__(self, character_id, network_client, is_main_character=False):
        super().__init__()
        self.character_id = character_id
        self.network_client = network_client

        self.screen_rect = Rect((0, 0), (0, 0))

        self.res_info = None

        self.target = (0, 0)
        self.target_list = []
        self.direction = 0
        self.is_new_target = False
        self.is_running = False

        self.mask = Mask(None, None)
        self.weapon = None

        self.is_mouse_over = False
        self.is_main_character = is_main_character

        self.load()

    def load(self):
        player_info = self.network_client.get_player(self.character_id)
        self.res_info = self.network_client.get_character(player_info["character"])
        self.x = player_info["position"][0]
        self.y = player_info["position"][1]
        self.target = (self.x, self.y)

    def reset_target(self):
        self.target = self.x, self.y


def character_factory(character_id, network_client, is_main_character=False):
    character = Character(character_id, network_client, is_main_character)
    print(is_main_character)
    if is_main_character:
        _state = state_factory(CharacterStandNormalState, [MainCharacterComponent, CharacterMouseComponent])
    else:
        _state = state_factory(CharacterStandNormalState, [CharacterMouseComponent])
    character.init_state(_state)
    return character
