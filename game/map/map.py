import pygame
from pygame.locals import *
from pygame.math import Vector2

from core.entity.game_object import GameObject
from core.state.state import state_factory
from game.map.map_state import MapState
from game.map.map_component import MapMouseComponent, MapReceiveComponent, MapPortalComponent

from settings import WindowSize


class Map(GameObject):
    def __init__(self, map_id, map_client, network_client):
        super().__init__(0, 0)
        self.map_client = map_client  # Map客户端
        self.network_client = network_client  # 网络客户端

        self.map_id = map_id  # scene/1001.map

        self.quest_timer = []
        self.unit_has_blitted = []
        self.surface = pygame.Surface(WindowSize)
        self.window = Rect((0, 0), WindowSize)

        self.inited = False
        self.ready = False
        self.mask = {}
        self.masks_of_unit = []

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

        self.target = (0, 0)

        self.init_state(MapState())

        self.state.add_component(MapMouseComponent())  # 地图操作组件
        self.state.add_component(MapReceiveComponent())  # 地图图片接收组件

        self.map_client.request_map_info(self.map_id)  # 获取地图基本信息

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

    def get_new_center(self, world_pc):
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
        return window_left + WindowSize[0]//2, window_top + WindowSize[1]//2

    def set_window(self, world_pc):
        tx, ty = self.get_new_center(world_pc)
        target_vector = Vector2()
        target_vector.x = tx
        target_vector.y = ty
        current_vector = Vector2()
        current_vector.x = self.window.centerx
        current_vector.y = self.window.centery
        new_vector = current_vector.slerp(target_vector, 0.05)
        self.window.move_ip(int(new_vector.x) - self.window.centerx, int(new_vector.y) - self.window.centery)
