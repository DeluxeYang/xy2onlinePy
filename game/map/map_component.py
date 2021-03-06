import numpy
import pygame
from pygame.locals import *
from io import BytesIO

from core.component.component import Component
from game.map.portal import portal_factory

from utils.mask import Mask

from core.world.director import director

from time import time

from settings import logger


class MapMouseComponent(Component):
    def on_mouse_right_down(self, event):
        left_top = self.state.game_object.get_left_top()
        self.state.game_object.map_client.request_find_path(
            self.state.game_object.map_id,
            director.account.get_main_role().get_xy(),
            (event.pos[0] + left_top[0], event.pos[1] + left_top[1]),
            is_running=True)

    def on_mouse_left_down(self, event):
        left_top = self.state.game_object.get_left_top()
        self.state.game_object.map_client.request_find_path(
            self.state.game_object.map_id,
            director.account.get_main_role().get_xy(),
            (event.pos[0]+left_top[0], event.pos[1]+left_top[1]),
            is_running=False)


class MapReceiveComponent(Component):
    def on_receive_map_info(self, event):
        if self.state.game_object.map_id == event.map_id:
            self.state.game_object.map_type = event.map_type
            self.state.game_object.map_width = event.map_width
            self.state.game_object.map_height = event.map_height
            self.state.game_object.unit_width = event.unit_width
            self.state.game_object.unit_height = event.unit_height
            self.state.game_object.col = event.col
            self.state.game_object.row = event.row
            self.state.game_object.n = event.n
            self.state.game_object.coordinate = event.coordinate
            self.state.game_object.surface = pygame.Surface((event.map_width, event.map_height))  # 整个地图Surface
            self.state.game_object.unit_has_blitted = [False for _ in range(event.n)]
            self.state.game_object.masks_of_unit = [[] for _ in range(event.n)]
            self.state.game_object.portals_of_unit = [[] for _ in range(event.n)]
            self.state.game_object.quest_timer = [0 for _ in range(event.n)]
            self.state.game_object.inited = True
            self.state.game_object.ready = True
            self.state.late_update()
            event.handled = True

    def on_receive_map_unit(self, event):
        logger.debug("Map Unit Receive:" + str(event.map_id) + " " + str(event.unit_num))
        if self.state.game_object.map_id == event.map_id:
            if not self.state.game_object.unit_has_blitted[event.unit_num]:
                self._blit_unit(event.jpeg, event.unit_num)  # 将图片blit
                masks = []
                for mask in event.masks:
                    try:
                        masks.append(self._generate_mask(mask))  # 生成Mask
                    except Exception as e:
                        print(e)
                self.state.game_object.masks_of_unit[event.unit_num] = masks  # 将该unit对应Mask放入对应位置
            event.handled = True

    def _blit_unit(self, jpg, unit_num):
        """
        将单元图片blit到MAP上
        :param jpg:
        :param unit_num:
        :return:
        """
        self.state.game_object.unit_has_blitted[unit_num] = True
        if self.state.game_object.map_type == 1:
            unit_image = pygame.image.frombuffer(jpg, (320, 240), "RGB")
        else:
            jpg_file = BytesIO(jpg)
            unit_image = pygame.image.load(jpg_file).convert()
        row = unit_num // self.state.game_object.col  # 行号
        col = unit_num % self.state.game_object.col  # 列号
        self.state.game_object.surface.blit(unit_image, (col * 320, row * 240))  # 把图贴到MAP上

    def _generate_mask(self, mask):
        """
        由mask的数组生成Surface，再生成mask
        :param mask:
        :return:
        """
        x, y = mask["x"], mask["y"]
        w, h = mask["w"], mask["h"]
        data = mask["data"]
        if (x, y) not in self.state.game_object.mask:
            align_w = (w // 4 + (w % 4 != 0)) * 4  # 4倍数化
            mask_array = numpy.frombuffer(data, dtype=numpy.int8)  # 将mask data转成numpy 数组
            mask_array.shape = h, align_w
            mask_array = numpy.transpose(mask_array)  # 转置
            _surface = pygame.surfarray.make_surface(mask_array).convert()  # 从数组中生成Surface
            _rect = Rect(x, y, w, h)  # 划定mask所占区域
            py_mask = pygame.mask.from_threshold(_surface, (0, 0, 255, 255), (10, 10, 10, 255))  # 255的是0x11
            collision_mask = pygame.mask.from_threshold(_surface, (0, 0, 85, 255), (10, 10, 10, 255))  # 85的是0x11
            self.state.game_object.mask[(x, y)] = Mask(_rect, py_mask, collision_mask)
        return self.state.game_object.mask[(x, y)]


class MapPortalComponent(Component):
    def on_receive_map_portals(self, event):
        if self.state.game_object.map_id == event.map_id:
            portals = self.state.game_object.network_client.get_map_portals(
                self.state.game_object.map_id)  # 获取所有portals
            for portal in portals:
                portal_instance = portal_factory(**portal)  # Portal实例

                col = portal["position"][0] // self.state.game_object.unit_width
                row = portal["position"][1] // self.state.game_object.unit_height
                n = row * self.state.game_object.col + col  # 属于第n个unit

                self.state.game_object.portals_of_unit[n].append(portal_instance)
            event.handled = True
