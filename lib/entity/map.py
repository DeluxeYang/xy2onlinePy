from io import BytesIO
import numpy
import pygame
from pygame.locals import *

from lib.entity.game_object import GameObject
from lib.component.map_component import *

from settings import WindowSize


class Map(GameObject):
    def __init__(self, map_id, map_client, network_client, *components):
        super().__init__(*components)
        self.map_client = map_client
        self.network_client = network_client

        self.map_id = map_id

        self.quest_timer = []
        self.unit_has_blitted = []
        self.surface = pygame.Surface(WindowSize)
        self.window = Rect((0, 0), WindowSize)

        self.inited = True
        self.mask = {}
        self.masks_of_unit = None

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


    def load(self):
        self._request_map_info()

    def quest(self):
        """
        寻求地图unit数据
        :return:
        """
        units_needed = self._quest_25()
        for i in units_needed:
            if not self.unit_has_blitted[i]:  # 如果该单元还没有数据
                if self.quest_timer[i] == 0:  # 且该单元还没有发送过请求
                    self._request_map_unit(i)
                self.quest_timer[i] = +1
                if self.quest_timer[i] == 5:  # 累计请求5次后重置为0
                    self.quest_timer[i] = 0

    def _request_map_info(self):
        send_data = {
            'request': "map_info",
            'map_id': self.map_id,
        }
        self.map_client.send(send_data)

    def _request_map_unit(self, unit_id):
        send_data = {
            'request': "map_unit",
            'map_id': self.map_id,
            'unit_num': unit_id
        }
        self.map_client.send(send_data)

    def find_path(self, mouse_pos, is_running):
        send_data = {
            'request': "find_path",
            'map_id': self.map_id,
            'current': self.window.center,
            'target': mouse_pos,
            'is_running': is_running
        }
        self.map_client.send(send_data)

    def update(self, dt):
        """
        场景帧更新，并生成场景地形mask
        :return:
        """
        no_repeat = {}
        masks = []
        units = self._quest_16(width_margin=60, height_margin=40)
        for i in units:
            for mask in self.masks_of_unit[i]:
                if (mask.rect.x, mask.rect.y) not in no_repeat:
                    no_repeat[(mask.rect.x, mask.rect.y)] = True
                    masks.append(mask)
        # data["mask_list"] = masks
        # data["window_left_top_pos"] = self.get_left_top()
        # data["collision_window"] = self.get_collision_window()

    def draw(self, screen):
        screen.blit(self.surface, (0, 0), self.window)

    def receive_map_info(self, data):
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
            self.surface = pygame.Surface((self.map_width, self.map_height))  # 整个地图Surface
            self.unit_has_blitted = [False for _ in range(self.n)]
            self.masks_of_unit = [[] for _ in range(self.n)]
            self.quest_timer = [0 for _ in range(self.n)]
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
        self.surface.blit(unit_image, (col * 320, row * 240))  # 把图贴到MAP上

    def _generate_mask(self, mask):
        """
        由mask的数组生成Surface，再生成mask
        :param mask:
        :return:
        """
        x, y = mask["x"], mask["y"]
        w, h = mask["w"], mask["h"]
        data = mask["data"]
        if (x, y) not in self.mask:
            align_w = (w // 4 + (w % 4 != 0)) * 4  # 4倍数化
            mask_array = numpy.frombuffer(data, dtype=numpy.int8)  # 将mask data转成numpy 数组
            mask_array.shape = h, align_w
            mask_array = numpy.transpose(mask_array)  # 转置
            _surface = pygame.surfarray.make_surface(mask_array).convert()  # 从数组中生成Surface
            _rect = Rect(x, y, w, h)  # 划定mask所占区域
            py_mask = pygame.mask.from_threshold(_surface, (0, 0, 255, 255), (10, 10, 10, 255))  # 255的是0x11
            collision_mask = pygame.mask.from_threshold(_surface, (0, 0, 85, 255), (10, 10, 10, 255))  # 85的是0x11
            self.mask[(x, y)] = Mask(_rect, py_mask, collision_mask)
        return self.mask[(x, y)]

    def _quest_25(self):
        row = self.window.centery // 240 if self.window.centery // 240 != self.row else self.window.centery // 240 - 1  # 向下取整
        col = self.window.centerx // 320 if self.window.centerx // 320 != self.col else self.window.centerx // 320 - 1  # 向下取整
        pos = int(row * self.col + col)  # 当前单元格
        _units = [pos]  # 正在
        left = right = up = down = 0
        if col == 0:  # 左1，右边+2
            _units += [pos + 1, pos + 2]
            right += 2
        elif col == 1:  # 左2， 右边+2， 左边+1
            _units += [pos - 1, pos + 1, pos + 2]
            right += 2
            left += 1
        elif col == self.col - 1:  # 靠右，左边+2
            _units += [pos - 1, pos - 2]
            left += 2
        elif col == self.col - 2:  # 右2，右边+1，左边+2
            _units += [pos + 1, pos - 1, pos - 2]
            right += 1
            left += 2
        else:
            _units += [pos + 1, pos + 2, pos - 1, pos - 2]
            right += 2
            left += 2

        if row == 0:
            _units += [pos + self.col, pos + self.col * 2]
            down += 2
        elif row == 1:
            _units += [pos - self.col, pos + self.col, pos + self.col * 2]
            up += 1
            down += 2
        elif row == self.row - 1:
            _units += [pos - self.col, pos - self.col * 2]
            up += 2
        elif row == self.row - 2:
            _units += [pos + self.col, pos - self.col, pos - self.col * 2]
            up += 2
            down += 1
        else:
            _units += [pos + self.col, pos + self.col * 2, pos - self.col, pos - self.col * 2]
            up += 2
            down += 2
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

    def _quest_16(self, width_margin=160, height_margin=120):
        """
        根据地图像素位置，获取需要的units_num
        :param width_margin:
        :param height_margin:
        :return:
        """
        row = self.window.centery // 240 if self.window.centery // 240 != self.row else self.window.centery // 240 - 1  # 向下取整
        col = self.window.centerx // 320 if self.window.centerx // 320 != self.col else self.window.centerx // 320 - 1  # 向下取整
        pos = int(row * self.col + col)  # 当前单元格
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
            if self.window.centerx % 320 >= 320 - width_margin and col + 2 <= self.col - 1:  # 单元格内靠右，则右边预读
                _units.append(pos + 2)
                right += 1
            elif self.window.centerx % 320 <= width_margin and col - 2 >= 0:  # 单元格内靠左，左边预读
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
            if self.window.centery % 240 >= 240 - height_margin and row + 2 <= self.row - 1:  # 单元格内靠下，则预读下面
                _units.append(pos + self.col * 2)
                down += 1
            elif self.window.centery % 240 <= height_margin and row - 2 >= 0:  # 单元格内靠上，则预读上面
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

    def get_world_pc(self, pos):
        """
        获得地图像素坐标
        :param pos:
        :return:
        """
        left, top = self.get_left_top()
        x = left + pos[0]  # 屏幕左上角地图绝对像素点 + 鼠标相对点 = 地图绝对点
        y = top + pos[1]
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


class Mask:
    def __init__(self, rect, mask, collision_mask=None):
        self.rect = rect
        self.mask = mask
        self.collision_mask = collision_mask


def map_factory(map_id, map_client, network_client):
    _map = Map(map_id, map_client, network_client)
    _map.load()
    _map.add_component(MapMouseComponent())
    _map.add_component(MapReceiveComponent())
    return _map