import pygame
from pygame.locals import *

from lib.entity.game_object import GameObject
from lib.component.map_component import MapMouseComponent, MapReceiveComponent,\
    MapUpdateComponent
from lib.state.map_state import MapState

from settings import WindowSize


class Map(GameObject):
    def __init__(self, map_id, map_client, network_client):
        super().__init__()
        self.map_client = map_client
        self.network_client = network_client

        self.map_id = map_id

        self.quest_timer = []
        self.unit_has_blitted = []
        self.surface = pygame.Surface(WindowSize)
        self.window = Rect((0, 0), WindowSize)

        self.inited = False
        self.ready = False
        self.mask = {}
        self.masks_of_unit = []
        self.portals = {}
        self.portals_of_unit = []

        self.left_top = (0, 0)
        self.me_world_pc = (0, 0)

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

        self.load()

    def load(self):
        self.map_client.request_map_info(self.map_id)
        self.portals = self.network_client.get_map_portals(self.map_id)

    def get_world_pc(self, screen_pos):
        """
        获得地图像素坐标
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
        return self.window.centerx, self.window.centery

    def get_left_top(self):
        return self.window.left, self.window.top

    def get_collision_window(self):
        return self.window.inflate(100, 100)  # 放大100像素

    def set_window(self, world_pc):
        """
        根据中心像素位置，获取显示窗口
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
        del self.window
        self.window = Rect((window_left, window_top), (WindowSize[0], WindowSize[1]))


def map_factory(map_id, map_client, network_client):
    _map = Map(map_id, map_client, network_client)
    _map.init_state(MapState())
    _map.add_component(MapMouseComponent())
    _map.add_component(MapReceiveComponent())
    _map.add_component(MapUpdateComponent())
    return _map
