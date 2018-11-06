import pygame
from pygame.locals import *

from .component import Component
from utils.math import is_same_coordinate, calc_direction_8, calc_direction_4

from lib.state.character_state import CharacterRunningState, CharacterWalkingState


class MainCharacterComponent(Component):
    def on_receive_path_list(self, event):
        self.game_object.target_list = event.path_list
        self.game_object.is_new_target = True
        self.game_object.is_running = event.is_running
        event.handled = True
        if self.game_object.is_running:
            self.game_object.changing_state(CharacterRunningState())
        else:
            self.game_object.changing_state(CharacterWalkingState())
