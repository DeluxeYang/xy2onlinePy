import pygame
from pygame.locals import *

from .component import Component
from utils.math import is_same_coordinate, calc_direction_8, calc_direction_4

from lib.state.character_state import CharacterRunningState, CharacterWalkingState

bright = pygame.Surface((400, 400), flags=pygame.SRCALPHA)
bright.fill((80, 80, 80, 0))

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

    def on_mouse_over(self, event):
        if self.is_mouse_focus_on(event):
            self.game_object.is_mouse_over = True
            event.handled = True

    def on_mouse_left_down(self, event):
        if self.is_mouse_focus_on(event):
            print(self.game_object.character_id)
            event.handled = True

    def on_mouse_right_down(self, event):
        if self.is_mouse_focus_on(event):
            event.handled = True

    def is_mouse_focus_on(self, event):
        if self.game_object.screen_rect.collidepoint(event.pos):
            offset_x = event.mouse_point_mask.rect.left - self.game_object.screen_rect.left
            offset_y = event.mouse_point_mask.rect.top - self.game_object.screen_rect.top
            if self.game_object.mask.mask.overlap(event.mouse_point_mask.mask, (offset_x, offset_y)):
                return True
        return False

    # def draw(self, screen=None):
    #     pygame.draw.rect(screen, (0, 0, 0), self.game_object.screen_rect)
