import pygame
from pygame.locals import *
import numpy
from io import BytesIO

from .component import Component
from utils.math import quest_16, quest_25


class MapMouseComponent(Component):
    def on_mouse_right_down(self, event):
        self.game_object.set_window(self.game_object.get_world_pc(event.pos))
        # self.game_object.find_path(event.pos, is_running=True)

    def on_mouse_left_down(self, event):
        left_top = self.game_object.get_left_top()
        self.game_object.map_client.request_find_path(self.game_object.map_id,
                                                      self.game_object.window.center,
                                                      (event.pos[0]+left_top[0], event.pos[1]+left_top[1]),
                                                      is_running=False)


class MapReceiveComponent(Component):
    def on_receive_map_info(self, event):
        if self.game_object.map_id == event.map_id:
            self.game_object.map_type = event.map_type
            self.game_object.map_width = event.map_width
            self.game_object.map_height = event.map_height
            self.game_object.unit_width = event.unit_width
            self.game_object.unit_height = event.unit_height
            self.game_object.col = event.col
            self.game_object.row = event.row
            self.game_object.n = event.n
            self.game_object.coordinate = event.coordinate
            self.game_object.surface = pygame.Surface((event.map_width, event.map_height))  # 整个地图Surface
            self.game_object.unit_has_blitted = [False for _ in range(event.n)]
            self.game_object.masks_of_unit = [[] for _ in range(event.n)]
            self.game_object.quest_timer = [0 for _ in range(event.n)]
            self.game_object.inited = True

            event.handled = True

    def on_receive_map_unit(self, event):
        if self.game_object.map_id == event.map_id:
            if not self.game_object.unit_has_blitted[event.unit_num]:
                self._blit_unit(event.jpeg, event.unit_num)  # 将图片blit
                masks = []
                for mask in event.masks:
                    try:
                        masks.append(self._generate_mask(mask))  # 生成Mask
                    except Exception as e:
                        print(e)
                self.game_object.masks_of_unit[event.unit_num] = masks  # 将该unit对应Mask放入对应位置
            event.handled = True

    def on_update_map_window(self, world_pc):
        pass

    def _blit_unit(self, jpg, unit_num):
        """
        将单元图片blit到MAP上
        :param jpg:
        :param unit_num:
        :return:
        """
        self.game_object.unit_has_blitted[unit_num] = True
        if self.game_object.map_type == 1:
            unit_image = pygame.image.frombuffer(jpg, (320, 240), "RGB")
        else:
            jpg_file = BytesIO(jpg)
            unit_image = pygame.image.load(jpg_file).convert()
        row = unit_num // self.game_object.col  # 行号
        col = unit_num % self.game_object.col  # 列号
        self.game_object.surface.blit(unit_image, (col * 320, row * 240))  # 把图贴到MAP上

    def _generate_mask(self, mask):
        """
        由mask的数组生成Surface，再生成mask
        :param mask:
        :return:
        """
        x, y = mask["x"], mask["y"]
        w, h = mask["w"], mask["h"]
        data = mask["data"]
        if (x, y) not in self.game_object.mask:
            align_w = (w // 4 + (w % 4 != 0)) * 4  # 4倍数化
            mask_array = numpy.frombuffer(data, dtype=numpy.int8)  # 将mask data转成numpy 数组
            mask_array.shape = h, align_w
            mask_array = numpy.transpose(mask_array)  # 转置
            _surface = pygame.surfarray.make_surface(mask_array).convert()  # 从数组中生成Surface
            _rect = Rect(x, y, w, h)  # 划定mask所占区域
            py_mask = pygame.mask.from_threshold(_surface, (0, 0, 255, 255), (10, 10, 10, 255))  # 255的是0x11
            collision_mask = pygame.mask.from_threshold(_surface, (0, 0, 85, 255), (10, 10, 10, 255))  # 85的是0x11
            self.game_object.mask[(x, y)] = Mask(_rect, py_mask, collision_mask)
        return self.game_object.mask[(x, y)]


class MapQuestComponent(Component):
    def early_update(self, data=None):
        units_needed = quest_25(self.game_object.window, self.game_object.row, self.game_object.col)
        for i in units_needed:
            if not self.game_object.unit_has_blitted[i]:  # 如果该单元还没有数据
                if self.game_object.quest_timer[i] == 0:  # 且该单元还没有发送过请求
                    self.game_object.map_client.request_map_unit(self.game_object.map_id, unit_num=i)
                self.game_object.quest_timer[i] = +1
                if self.game_object.quest_timer[i] == 5:  # 累计请求5次后重置为0
                    self.game_object.quest_timer[i] = 0


class Mask:
    def __init__(self, rect, mask, collision_mask=None):
        self.rect = rect
        self.mask = mask
        self.collision_mask = collision_mask