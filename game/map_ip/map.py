import pygame
from pygame.locals import *
from pygame.math import Vector2

from core.entity.game_object import GameObject

from utils.map_x import MapX
from game.map_ip.map_state import MapState
from game.map_ip.map_component import MapMouseComponent

from settings import WindowSize


class Map(GameObject):
    def __init__(self, map_version, map_id, world_pc):
        super(Map, self).__init__(0, 0)
        self.map_version = map_version
        self.map_id = map_id  # scene/1001.map
        self.map_path = map_version + '/' + str(map_id) + '.map'

        self.unit_has_blitted = []  # 记录哪些unit已经加载完成了
        self.surface = pygame.Surface(WindowSize)
        self.window = Rect(world_pc, WindowSize)

        self.mask = {}
        self.masks_of_unit = []

        self.left_top = (0, 0)

        self.map_x = MapX(self.map_path)

        self.init_state(MapState())
        self.state.add_component(MapMouseComponent())  # 地图操作组件

        self.init()

        self.set_window(world_pc, directly=True)

    def init(self):
        self.surface = pygame.Surface((self.map_x.map_width, self.map_x.map_height))  # 整个地图Surface
        self.unit_has_blitted = [False for _ in range(self.map_x.n)]
        self.masks_of_unit = [[] for _ in range(self.map_x.n)]
        self.inited = True
        self.ready = True

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
        elif x > self.map_x.map_width:
            x = self.map_x.map_width
        if y < 0:
            y = 0
        elif y > self.map_x.map_height:
            y = self.map_x.map_height
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

    def get_new_center(self, world_pc):
        """
        根据人物世界坐标，将地图中心限制在有效的视窗范围内
        :param world_pc:
        :return: 在有效的视窗范围内的地图中心
        """
        window_left = world_pc[0] - WindowSize[0] // 2
        window_right = world_pc[0] + WindowSize[0] // 2
        if window_left < 0:
            window_left = 0
        elif window_right > self.map_x.map_width:
            window_left = self.map_x.map_width - WindowSize[0]
        window_top = world_pc[1] - WindowSize[1] // 2
        window_bottom = world_pc[1] + WindowSize[1] // 2
        if window_top < 0:
            window_top = 0
        elif window_bottom > self.map_x.map_height:
            window_top = self.map_x.map_height - WindowSize[1]
        return window_left + WindowSize[0]//2, window_top + WindowSize[1]//2

    def set_window(self, world_pc, directly=False):
        """
        根据人物世界坐标，以线性差值的方式，使视窗跟随人物
        :return:
        """
        tx, ty = self.get_new_center(world_pc)
        target_vector = Vector2()
        target_vector.x = tx
        target_vector.y = ty
        current_vector = Vector2()
        current_vector.x = self.window.centerx
        current_vector.y = self.window.centery
        if directly:
            self.window.move_ip(int(target_vector.x) - self.window.centerx, int(target_vector.y) - self.window.centery)
        else:
            new_vector = current_vector.slerp(target_vector, 0.05)
            self.window.move_ip(int(new_vector.x) - self.window.centerx, int(new_vector.y) - self.window.centery)
