import pygame
from pygame.locals import *

from core.state.animation_state import AnimationState
from settings import ResMargin



class MaterialAnimationState(AnimationState):
    def register(self, obj):
        """
        绑定GameObject
        :param obj:
        :return:
        """
        super().register(obj)
        address = self.game_object.res_info[self.res_index]
        self.res_init(address)  # 初始化res

    def update(self, data):
        one_loop = super().update(data)
        self.set_surface(self.game_object.direction)
        return one_loop

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.game_object.surface, self.game_object.screen_rect)
