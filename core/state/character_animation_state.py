import pygame
from pygame.locals import *

from core.state.animation_state import AnimationState
from settings import ResMargin


bright = pygame.Surface((400, 400), flags=pygame.SRCALPHA)
bright.fill((80, 80, 80, 0))
ResMargin_2 = ResMargin * 2


class CharacterAnimationState(AnimationState):
    def register(self, obj):
        """
        绑定GameObject
        :param obj:
        :return:
        """
        super().register(obj)
        if isinstance(self.res_index, list):  # ["weapon", "knife", "run"]
            address = self.game_object.res_info
            for x in self.res_index:
                address = address[x]
        else:
            address = self.game_object.res_info[self.res_index]
        self.res_init(address)  # 初始化res

    def update(self, data):
        one_loop = super().update(data)
        self.game_object.mask = self.get_mask(self.game_object.direction)  # 设定shape对应的mask
        self.set_surface(self.game_object.direction, data["other_masks"], self.game_object.get_xy())
        return one_loop

    def draw(self, screen):
        super().draw(screen)
        surface = self.game_object.surface.copy()
        if self.game_object.is_mouse_over:
            surface.blit(bright, (0, 0), special_flags=BLEND_RGB_ADD)
            self.game_object.is_mouse_over = False
        screen.blit(surface, self.game_object.screen_rect)
