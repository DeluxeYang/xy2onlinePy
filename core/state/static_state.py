import pygame
from pygame.locals import *

from core.state.state import State
from utils.res_manager import res_manager
from settings import ResMargin

ResMargin_2 = ResMargin * 2


class StaticState(State):
    res_index = "normal"

    def __init__(self):
        super().__init__()
        self.res = None

    def register(self, obj):
        super().register(obj)
        address = self.game_object.res_info[self.res_index]
        self.res = res_manager.get_res(address[0], address[1])
        self.game_object.surface = self.res.image_group[0][0].copy()
        self.game_object.inited = True

    def update(self, data):
        self.game_object.screen_rect = self.get_screen_rect(data["left_top"])  # 根据shape的World 坐标和left_top，确定相对屏幕坐标
        self.game_object.ready = True  # ready
        super().update(data)

    def draw(self, screen):
        super().draw(screen)  # State的draw 即调用组件draw
        screen.blit(self.game_object.surface, self.game_object.screen_rect)

    def get_screen_rect(self, left_top):
        world_rect = self.get_world_rect()
        return world_rect.move(-left_top[0], -left_top[1])

    def get_world_rect(self):
        x = int(self.game_object.x) - ResMargin - self.res.x
        y = int(self.game_object.y) - ResMargin - self.res.y
        w = self.res.w + ResMargin_2
        h = self.res.h + ResMargin_2
        return Rect(x, y, w, h)