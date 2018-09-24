
import numpy
from io import BytesIO

import pygame
from pygame.locals import *

from Settings import *
from utils.Mask import Mask

from res.MapInfo import map_info


class Scene:
    def __init__(self, map_name):
        """
        初始化场景Scene
        :param map_name:  MapInfo中的地图ID
        """
        self.inited = False
        self.map_info = map_info[map_name]  # 地图信息
        self.map_id = self.map_info["map_file"].split("/")[-1]  # 记录Map编号

        self.x = 0
        self.y = 0
        self.left = 0
        self.top = 0

        self.MAP = None
        self.MASK = {}
        self.masks_of_unit = None
        self.unit_has_blitted = []
        self.quest_clock = []

        self.map_type = 0
        self.map_width = 0
        self.map_height = 0
        self.unit_width = 0
        self.unit_height = 0
        self.col = 0
        self.row = 0
        self.n = 0
        self.coordinate = None

    def update(self):
        """
        场景帧更新
        :return: 返回window_left_top和地形Mask
        """
        no_repeat = {}
        masks = []
        units = self._pixel_to_units_num(width_margin=60, height_margin=40)
        for i in units:
            for mask in self.masks_of_unit[i]:
                if (mask.rect.x, mask.rect.y) not in no_repeat:
                    no_repeat[(mask.rect.x, mask.rect.y)] = True
                    masks.append(mask)
        self._blit()
        return masks

    def quest(self, client):
        """
        寻求地图unit数据
        :return:
        """
        units_needed = self._pixel_to_units_num()
        for i in units_needed:
            if not self.unit_has_blitted[i]:  # 如果该单元还没有数据
                if self.quest_clock[i] == 0:  # 且该单元还没有发送过请求
                    self.get_map_unit(client, i)
                self.quest_clock[i] = +1
                if self.quest_clock[i] == 5:  # 累计请求5次后重置为0
                    self.quest_clock[i] = 0

    def get_map(self, client):
        """
        异步获取地图信息
        :return:
        """
        client.get_map_info(self.map_info["map_file"])

    def get_map_unit(self, client, unit_num):
        """
        异步获取地图unit数据
        :return:
        """
        client.get_map_unit(self.map_info["map_file"], unit_num)

    def receive_map(self, data):
        """
        异步获取地图信息回调
        :param data:
        :return:
        """
        if self.map_id == data["map_id"]:
            self.map_type = data["map_type"]
            self.map_width = data["map_width"]
            self.map_height = data["map_height"]
            self.unit_width = data["unit_width"]
            self.unit_height = data["unit_height"]
            self.col = data["col"]
            self.row = data["row"]
            self.n = data["n"]
            self.coordinate = data["coordinate"]
            self.MAP = pygame.Surface((self.map_width, self.map_height))  # 整个地图Surface
            self.unit_has_blitted = [False for _ in range(self.n)]
            self.masks_of_unit = [[] for _ in range(self.n)]
            self.quest_clock = [0 for _ in range(self.n)]
            self.inited = True

    def receive_map_unit(self, data):
        """
        异步获取地图unit数据回调
        :param data:
        :return:
        """
        if self.map_id == data["map_id"]:
            if not self.unit_has_blitted[data["unit_num"]]:
                self._blit_unit(data["jpg"], data["unit_num"])  # 将图片blit
                masks = []
                for mask in data["masks"]:
                    try:
                        masks.append(self._generate_mask(mask))  # 生成Mask
                    except Exception as e:
                        print(e)
                self.masks_of_unit[data["unit_num"]] = masks  # 将该unit对应Mask放入对应位置

    def set_xy(self, mouse_pos):
        """
        获得地图像素坐标
        :param mouse_pos:
        :return:
        """
        x = self.left + mouse_pos[0]  # 屏幕左上角地图绝对像素点 + 鼠标相对点 = 地图绝对点
        y = self.top + mouse_pos[1]
        if x < 0:
            self.x = 0
        elif x > self.map_width:
            self.x = self.map_width
        else:
            self.x = x
        if y < 0:
            self.y = 0
        elif y > self.map_height:
            self.y = self.map_height
        else:
            self.y = y

    def get_xy(self):
        return self.x, self.y

    def get_left_top(self):
        return self.left, self.top

    def _blit_unit(self, jpg, unit_num):
        """
        将单元图片blit到MAP上
        :param jpg:
        :param unit_num:
        :return:
        """
        self.unit_has_blitted[unit_num] = True
        if self.map_type == 1:
            unit_image = pygame.image.frombuffer(jpg, (320, 240), "RGB")
        else:
            jpg_file = BytesIO(jpg)
            unit_image = pygame.image.load(jpg_file).convert()
        row = unit_num // self.col  # 行号
        col = unit_num % self.col  # 列号
        self.MAP.blit(unit_image, (col * 320, row * 240))  # 把图贴到MAP上

    def _generate_mask(self, mask):
        """
        由mask的数组生成Surface，再生成mask
        :param mask:
        :return:
        """
        x, y = mask["x"], mask["y"]
        w, h = mask["w"], mask["h"]
        data = mask["data"]
        if (x, y) not in self.MASK:
            align_w = (w // 4 + (w % 4 != 0)) * 4  # 4倍数化
            mask_array = numpy.frombuffer(data, dtype=numpy.int8)  # 将mask data转成numpy 数组
            mask_array.shape = h, align_w
            mask_array = numpy.transpose(mask_array)  # 转置
            _surface = pygame.surfarray.make_surface(mask_array).convert()  # 从数组中生成Surface
            _rect = Rect(x, y, w, h)  # 划定mask所占区域
            py_mask = pygame.mask.from_threshold(_surface, (0, 0, 255, 255), (10, 10, 10, 255))  # 255的是0x11
            collision_mask = pygame.mask.from_threshold(_surface, (0, 0, 85, 255), (10, 10, 10, 255))  # 85的是0x11
            self.MASK[(x, y)] = Mask(_rect, py_mask, collision_mask)
        return self.MASK[(x, y)]

    def _get_window(self):
        """
        根据中心像素位置，获取显示窗口
        :return:
        """
        window_left = self.x - Window_Size[0] // 2
        window_right = self.x + Window_Size[0] // 2
        if window_left < 0:
            window_right = Window_Size[0]
            window_left = 0
        elif window_right > self.map_width:
            window_right = self.map_width
            window_left = self.map_width - Window_Size[0]
        window_top = self.y - Window_Size[1] // 2
        window_bottom = self.y + Window_Size[1] // 2
        if window_top < 0:
            window_top = 0
            window_bottom = Window_Size[1]
        elif window_bottom > self.map_height:
            window_top = self.map_height - Window_Size[1]
            window_bottom = self.map_height
        window = Rect((window_left, window_top), (window_right, window_bottom))
        return window

    def _pixel_to_units_num(self, width_margin=160, height_margin=120):
        """
        根据地图像素位置，获取需要的units_num
        :param width_margin:
        :param height_margin:
        :return:
        """
        row = self.y // 240 if self.y // 240 != self.row else self.y // 240 - 1  # 向下取整
        col = self.x // 320 if self.x // 320 != self.col else self.x // 320 - 1  # 向下取整
        pos = row * self.col + col  # 当前单元格
        _units = [pos]  # 正在
        left = right = up = down = 0
        if col == 0:  # 靠左，就把右边的单元格放进来
            _units.append(pos + 1)
            right += 1
            if col + 2 <= self.col - 1:
                _units.append(pos + 2)
                right += 1
        elif col == self.col - 1:  # 靠右，就把左边的单元格放进来
            _units.append(pos - 1)
            left += 1
            if col - 2 >= 0:
                _units.append(pos - 2)
                left += 1
        else:  # 中间
            _units += [pos + 1, pos - 1]
            left = right = 1
            if self.x % 320 >= 320 - width_margin and col + 2 <= self.col - 1:  # 单元格内靠右，则右边预读
                _units.append(pos + 2)
                right += 1
            elif self.x % 320 <= width_margin and col - 2 >= 0:  # 单元格内靠左，左边预读
                _units.append(pos - 2)
                left += 1

        if row == 0:  # 靠上，则把下面的格子放进来
            _units.append(pos + self.col)
            down += 1
            if row + 2 <= self.row - 1:
                _units.append(pos + self.col * 2)
                down += 1
        elif row == self.row - 1:  # 靠下，则把上面的格子放进来
            _units.append(pos - self.col)
            up += 1
            if row - 2 >= 0:
                _units.append(pos - self.col * 2)
                up += 1
        else:
            _units += [pos + self.col, pos - self.col]
            up = down = 1
            if self.y % 240 >= 240 - height_margin and row + 2 <= self.row - 1:  # 单元格内靠下，则预读下面
                _units.append(pos + self.col * 2)
                down += 1
            elif self.y % 240 <= height_margin and row - 2 >= 0:  # 单元格内靠上，则预读上面
                _units.append(pos - self.col * 2)
                up += 1
        if left * up > 0:
            for i in range(1, left + 1):
                for j in range(1, up + 1):
                    _units.append((pos - i) - self.col * j)
        if left * down > 0:
            for i in range(1, left + 1):
                for j in range(1, down + 1):
                    _units.append((pos - i) + self.col * j)
        if right * up > 0:
            for i in range(1, right + 1):
                for j in range(1, up + 1):
                    _units.append((pos + i) - self.col * j)
        if right * down > 0:
            for i in range(1, right + 1):
                for j in range(1, down + 1):
                    _units.append((pos + i) + self.col * j)
        _units.sort()
        return _units

    def _blit(self):
        """
        将MAP blit到屏幕上
        :return:
        """
        window_rect = self._get_window()
        _screen = pygame.display.get_surface()
        _screen.blit(self.MAP, (0, 0), window_rect)
        self.left = window_rect.left
        self.top = window_rect.top
