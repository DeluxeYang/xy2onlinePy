from pygame.locals import *

from res.characters import characters
from utils.mask import Mask

from core.entity.game_object import GameObject
from core.state.state import state_factory
from game.character.character_state import CharacterStandNormalState
from game.character.character_component import MainCharacterComponent, CharacterMouseComponent


class Role(GameObject):
    def __init__(self, role_name):
        super().__init__(0, 0)

        self.is_main = False

        self.name = role_name

        self.level = None
        self.reborn = None

        self.race = None
        self.version = None
        self.character = None

        self.map_id = None
        self.x = None
        self.y = None

        self.state = state_factory(CharacterStandNormalState, [CharacterMouseComponent])

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

    @property
    def is_main_role(self):
        return self.is_main

    @is_main_role.setter
    def is_main_role(self, value):
        if self.is_main_role == value:
            return
        self.is_main = value
        if self.is_main_role:
            _state = state_factory(CharacterStandNormalState, [MainCharacterComponent, CharacterMouseComponent])
        else:
            _state = state_factory(CharacterStandNormalState, [CharacterMouseComponent])
        self.changing_state(_state)

    def specify(self, level, reborn,
                race, version, character,
                map_id, x, y):
        self.res_info = characters[race][version][character]

        self.level = level
        self.reborn = reborn

        self.race = race
        self.version = version
        self.character = character

        self.map_id = map_id
        self.x = x
        self.y = y

    def get_xy(self):
        return self.x, self.y

    def set_xy(self, x, y):
        self.x = x
        self.y = y

    def reset_target(self):
        self.target = self.x, self.y
