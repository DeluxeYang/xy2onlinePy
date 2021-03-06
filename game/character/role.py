from pygame.locals import *

from res.characters import characters
from utils.mask import Mask

from core.entity.game_object import GameObject
from core.state.state import state_factory
from game.character.character_state import CharacterStandNormalState
from game.character.character_component import MainCharacterComponent, CharacterMouseComponent


class Role(GameObject):
    race_names = {'ren': '人', 'mo': '魔', 'xian': '仙', 'gui': '鬼'}
    gender_choices = ['女', '男']

    def __init__(self, _id, name, level, reborn, race, version, character, gender):
        super().__init__(0, 0)

        self.is_main = False

        self.id = _id
        self.name = name

        self.level = level
        self.reborn = reborn
        self.gender = gender

        self.race = race
        self.version = version
        self.character = character
        self.res_info = characters[self.race][self.version][self.character]

        self.map_id = None
        self.map_version = ''
        self.x = None
        self.y = None

        self.state = state_factory(CharacterStandNormalState, [CharacterMouseComponent])
        self.init_state(self.state)

        self.screen_rect = Rect((0, 0), (0, 0))

        self.target = (0, 0)
        self.target_list = []
        self.direction = 0
        self.is_new_target = False
        self.is_running = False

        self.mask = Mask(None, None)
        self.weapon = None

        self.is_mouse_over = False

        self.inited = True
        self.ready = True

    @property
    def is_main_role(self):
        return self.is_main

    @is_main_role.setter
    def is_main_role(self, value):
        if self.is_main == value:
            return
        self.is_main = value
        if self.is_main_role:
            _state = state_factory(type(self.state), [MainCharacterComponent, CharacterMouseComponent])
        else:
            _state = state_factory(type(self.state), [CharacterMouseComponent])
        self.changing_state(_state, force=True)

    def locate(self, map_id, map_version, x, y):
        self.map_id = map_id
        self.map_version = map_version
        self.x = x
        self.y = y

    def get_xy(self):
        return self.x, self.y

    def set_xy(self, x, y):
        self.x = x
        self.y = y

    def reset_target(self):
        self.target = self.x, self.y
