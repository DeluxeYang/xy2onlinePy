import pygame
from pygame.locals import *

from core.entity.game_object import GameObject
from core.state.state import state_factory
from game.map.map_state import MapState
from game.map.map_component import MapMouseComponent, MapReceiveComponent, MapPortalComponent

from settings import WindowSize


class Map(GameObject):
    def __init__(self, map_id):
        super(Map, self).__init__(0, 0)
        self.map_id = map_id

        self.surface = pygame.Surface(WindowSize)
        self.window = Rect((0, 0), WindowSize)

        self.mask = {}
        self.masks_of_unit = []
        self.unit_has_blitted = []

        self.left_top = (0, 0)

        self.map_type = 0
        self.map_width = 0
        self.map_height = 0
        self.unit_width = 0
        self.unit_height = 0
        self.col = 0
        self.row = 0
        self.n = 0
        self.coordinate = None

    def get_world_pc(self, screen_pos):
        """
        由屏幕坐标转换为地图世界坐标
        :param screen_pos:
        :return:
        """
        left, top = self.get_left_top()
        x = left + screen_pos[0]  # 屏幕左上角地图绝对像素点 + 鼠标相对点 = 地图绝对点
        y = top + screen_pos[1]
        if x < 0:
            x = 0
        elif x > self.map_width:
            x = self.map_width
        if y < 0:
            y = 0
        elif y > self.map_height:
            y = self.map_height
        return x, y

    def get_center(self):
        """
        获取屏幕中心点坐标
        :return:
        """
        return self.window.centerx, self.window.centery

    def get_left_top(self):
        """
        获取屏幕左上角坐标
        :return:
        """
        return self.window.left, self.window.top

    def get_collision_window(self):
        """
        获取碰撞窗口
        :return:
        """
        return self.window.inflate(100, 100)  # 放大100像素

    def set_window(self, world_pc):
        """
        根据中心像素位置，获取显示窗口范围
        :return:
        """
        window_left = world_pc[0] - WindowSize[0] // 2
        window_right = world_pc[0] + WindowSize[0] // 2
        if window_left < 0:
            window_left = 0
        elif window_right > self.map_width:
            window_left = self.map_width - WindowSize[0]
        window_top = world_pc[1] - WindowSize[1] // 2
        window_bottom = world_pc[1] + WindowSize[1] // 2
        if window_top < 0:
            window_top = 0
        elif window_bottom > self.map_height:
            window_top = self.map_height - WindowSize[1]
        self.window = Rect((window_left, window_top), (WindowSize[0], WindowSize[1]))

