# -*- coding: utf-8 -*-
import numpy
import binascii
from utils.xy2_res import *
from utils.path_finding import AStar
from utils.pyastar import astar_path
from settings import XY2PATH


class Mask:
    def __init__(self, x, y, w, h, size=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.size = size
        self.data = None
        self.file_pos = 0


class MapX:
    def __init__(self, path):
        self.map_id = path
        self.map_type = 0  # 地图类型，1旧地图，2新地图
        self.unit_offset = []  # 地图各单元索引
        self.pic = []  # 各单元解压缩后的图片RGB字节
        self.mask = []  # Mask数据
        self.mask_num = 0  # Mask数量
        self.mask_offset = []  # 新地图中Mask的索引
        self.block = []  #
        self.cell = None  # 地图规则
        self.brig = []  # 光亮规则
        self.hand = None  # 地图文件File
        self.map_width = 0  # 地图宽
        self.map_height = 0  # 地图高
        self.unit_width = 320  # 单元宽
        self.unit_height = 240  # 单元高
        self.col = 0  # 列数，即每行有多少个单元
        self.row = 0  # 行数，即每列有多少个单元
        self.n = 0  # 单元总数
        self.map_size = 0  # 地图大小
        self.jpg_head = bytes()  # 旧地图中JPEG头
        self.coordinate = (0, 0)  # 地图中游戏坐标最大值
        self._open(XY2PATH + path)

        self._read_all_cells()
        # self.a_star = AStar(self.cell)
        # self.find_path = self.a_star.find_path

    def find_path(self, source, target):
        start = (int(source[1]) // 20, int(source[0] // 20))  # 初始坐标由像素地图坐标转为游戏坐标
        goal = (int(target[1] // 20), int(target[0] // 20))
        flag = True
        if 0 <= goal[0] < self.cell.shape[0] and 0 <= goal[1] < self.cell.shape[1]:
            if self.cell[goal[0], goal[1]] > 1:
                flag = False
                goal = self.nearest_valid_coord(goal)
        path = astar_path(self.cell, start, goal, allow_diagonal=True)
        print(path)
        path_list = self.adjust_path(path)  # 去除多余点, 同时将游戏坐标转为地图像素坐标
        if flag and len(path_list) > 0:
            path_list[-1] = target  # 将最后一个坐标，设为target_pc
        print(start, goal, path_list)
        return path_list

    def nearest_valid_coord(self, point):
        """
        获取离障碍点最近的可达点，广度搜索该点的四周
        :param point:
        :return:
        """
        _stack = [point]
        been = {}
        neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        while _stack:
            _point = _stack.pop(0)
            if self.cell[_point[0]][_point[1]] == 1:
                return _point
            been[_point] = 1
            for n in neighbors:
                temp = _point[0]+n[0], _point[1]+n[1]
                if temp not in been:
                    if 0 <= temp[0] < self.cell.shape[0] and 0 <= temp[1] < self.cell.shape[1]:
                        _stack.append(temp)
                        been[temp] = 1

    def adjust_path(self, path):
        """
        如果两个点之间没有阻碍，则抛弃他们之间点
        :param path:
        :return:
        """
        left = 0
        right = len(path) - 1
        _path = []
        while left < right:
            x1 = path[left][0]
            y1 = path[left][1]
            x2 = path[right][0]
            y2 = path[right][1]
            if self.is_obstacle_in_between(x1, y1, x2, y2):
                right -= 1  # 有阻碍，则right - 1，检验前一个点
                continue
            _path.append((path[right][1] * 20 + 10, path[right][0] * 20 + 10))  # 没有阻碍，则可直接到这个点
            left = right
            right = len(path) - 1
        return _path

    def is_obstacle_in_between(self, x1, y1, x2, y2):
        """
        查看两点之间是否有阻碍，有则返回True
        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :return:
        """
        f = self.generate_function(x1, y1, x2, y2)
        anti_f = self.generate_function(y1, x1, y2, x2)
        for x in range(min(x1, x2) + 1, max(x1, x2)):
            if self.cell[x, int(f(x)) + 1] > 1:
                return True
        for y in range(min(y1, y2) + 1, max(y1, y2)):
            if self.cell[int(anti_f(y)), y] > 1:
                return True
        return False

    @staticmethod
    def generate_function(x1, y1, x2, y2):
        def f(x):
            return y1 + ((x - x1) * (y2 - y1)) / (x2 - x1)
        return f

    def _open(self, path):
        """
        打开地图文件，记录地图单元索引数据
        :param path:
        :return:
        """
        try:
            self.hand = open(path, 'rb')
        except FileNotFoundError:
            raise Exception("找不到地图")
        else:
            map_sign = self._read_bytes_to_hex_list(4)  # map标识
            if map_sign == ['30', '2e', '31', '4d']:   # 大话2新地图
                self.map_type = 2
            elif map_sign == ['58', '50', '41', '4d']:  # 大话2旧地图
                self.map_type = 1
            else:
                raise Exception("地图类型错误")
            self.map_width = self._read_bytes_to_int(4)  # 地图总宽
            self.map_height = self._read_bytes_to_int(4)  # 地图总高
            self.coordinate = (self.map_width//20, self.map_height//20)  # 游戏坐标与像素的比例是1:20
            temp_col = self.map_width / self.unit_width
            self.col = int(temp_col) if temp_col == int(temp_col) else int(temp_col) + 1  # 地图列数
            temp_row = self.map_height / self.unit_height
            self.row = int(temp_row) if temp_row == int(temp_row) else int(temp_row) + 1  # 地图行数
            self.n = self.col * self.row  # 地图单元Unit数

            self.unit_offset = [self._read_bytes_to_int(4) for _ in range(self.n)]  # 地图单元Unit偏移
            self.pic = [None for _ in range(self.n)]  # 初始化各单元图片列表
            self.mask = [[] for _ in range(self.n)]  # 初始化各单元mask列表
            self.cell = numpy.ones((self.map_height // 20, self.map_width // 20), dtype=numpy.float32)

            if self.map_type == 1:  # 大话2旧地图
                self.map_size = self._read_bytes_to_int(4)  # 地图文件大小
                if self._read_bytes_to_hex_list(4) == ['48', '47', '50', '4a']:  # H G P J
                    size = self._read_bytes_to_int(4)
                    self.jpg_head = self.hand.read(size)
            elif self.map_type == 2:  # 大话2新地图
                self.hand.seek(4, 1)  # 跳过4字节
                self.mask_num = self._read_bytes_to_int(4)
                for _ in range(self.mask_num):
                    self.mask_offset.append(self._read_bytes_to_int(4))
                self._read_masks_in_new_map()

    def read_unit(self, unit_num):
        """
        读取地图特定单元
        :param unit_num: 地图单元索引号
        :return:
        """
        file_pos = self.unit_offset[unit_num]
        self.hand.seek(file_pos)  # 寻址
        unit_head_size = self._read_bytes_to_int(4)  # unit头
        if self.map_type == 2:  # 如果是新地图，需要跳过unit头
            if unit_head_size != 0:
                self.hand.seek(unit_head_size * 4, 1)  # 跳过unit头
        jpeg = None
        masks = []
        loop = True
        while loop:
            try:
                _sign = self._read_bytes_to_hex_list(4)
                _size = self._read_bytes_to_int(4)
                if _sign == ['47', '45', '50', '4a']:  # G E P J
                    jpeg = self._read_jpeg(_size)  # 读取jpeg数据
                elif _sign == ['47', '41', '4d', '49']:  # G A M I image
                    pass
                elif _sign == ['32', '53', '41', '4d']:  # 2 S A M mask
                    res = self._read_mask(_size, unit_num)
                    masks.append(res)  # 读取旧地图mask数据
                elif _sign == ['4b', '53', '41', '4d']:  # K S A M mask
                    res = self._read_mask(_size, unit_num)
                    masks.append(res)  # 读取旧地图mask数据
                elif _sign == ['4b', '4f', '4c', '42']:  # K O L B block
                    self.hand.seek(_size, 1)  # 不读取block数据，没用
                elif _sign == ['4c', '4c', '45', '43']:  # L L E C cell
                    self.hand.seek(_size, 1)  # 不读取cell，因为前面已经读过了
                elif _sign == ['47', '49', '52', '42']:  # G I R B brig
                    self.hand.seek(_size, 1)  # 光照阴影数据，先不读取
                elif _sign == ['20c', '44', '4e', '45']:
                    loop = False
                else:
                    loop = False
            except ValueError:
                break
        if self.map_type == 2:  # 如果是新地图
            for _mask in self.mask[unit_num]:  # 该unit里的mask已经被预读到self.mask[unit_num]中了
                align_w = _mask.w // 4 + (_mask.w % 4 != 0)
                out_size = align_w * _mask.h
                self.hand.seek(_mask.file_pos)
                _data = self.hand.read(_mask.size)
                _bytes = decompress_mask(_data, out_size)  # 解压mask数据
                res = {"x": _mask.x, "y": _mask.y, "w": _mask.w, "h": _mask.h, "data": _bytes}
                masks.append(res)
        return jpeg, masks

    def _read_jpeg(self, size):
        """
        读取单元内jpeg数据
        :param size:  数据大小
        :return:
        """
        if self.map_type == 1:  # 旧地图
            pic = self.hand.read(size)  # JPEG数据
            return read_old_map_to_rgb(self.jpg_head + pic + b"\xff\xd9")
        elif self.map_type == 2:
            pic = self._repair_new_jpg(self._read_bytes_to_hex_list(size))  # 修复为完整JPEG
            return self._hex_list_to_bytes(pic)

    def _read_mask(self, size, unit_num):
        """
        旧地图MASK读取方法。因为旧地图每个unit都会包含本unit里的的mask，因此是完全按需读取。
        :param size:
        :param unit_num: 需要unit_num来确定mask的map像素位置
        :return: MASK实例
        """
        x = self._read_bytes_to_int(4)
        y = self._read_bytes_to_int(4)
        w = self._read_bytes_to_int(4)  # mask宽
        h = self._read_bytes_to_int(4)  # mask高
        row = unit_num // self.col
        col = unit_num % self.col
        x_of_map = col * 320 + x  # mask关键点x
        y_of_map = row * 240 + y  # mask关键点y
        data = self.hand.read(size - 16)  # 读取MASK压缩数据，大小需要减去4 * 4
        align_w = w // 4 + (w % 4 != 0)  # 每字节包含4个像素，需要对齐
        out_size = align_w * h
        _bytes = decompress_mask(data, out_size)  # 解压mask数据
        return {"x": x_of_map, "y": y_of_map, "w": w, "h": h, "data": _bytes}

    def _read_all_cells(self):
        for unit_num in range(self.n):
            pos = self.unit_offset[unit_num]
            self.hand.seek(pos)  # 寻址
            unit_head_size = self._read_bytes_to_int(4)  # unit头
            if self.map_type == 2:  # 如果是新地图，需要跳过unit头
                if unit_head_size != 0:
                    self.hand.seek(unit_head_size * 4, 1)  # 跳过unit头
            row = unit_num // self.col  # 行号
            col = unit_num % self.col  # 列号
            while True:
                _sign = self._read_bytes_to_hex_list(4)
                _size = self._read_bytes_to_int(4)
                if _sign == ['4c', '4c', '45', '43']:  # L L E C cell
                    cell_list = self._read_bytes_to_int_list(_size)
                    i = j = 0
                    for one in cell_list:
                        if one == 1:
                            self.cell[row * 12 + i, col * 16 + j] = 99999.0
                        j += 1
                        if j >= 16:
                            j = 0
                            i += 1
                    break
                elif _sign == ["00", "00", "00", "00"]:
                    break
                else:
                    self.hand.seek(_size, 1)

    def _read_masks_in_new_map(self):
        for pos in self.mask_offset:
            self.hand.seek(pos)  # 寻址
            x = self._read_bytes_to_int(4)
            y = self._read_bytes_to_int(4)
            w = self._read_bytes_to_int(4)
            h = self._read_bytes_to_int(4)
            size = self._read_bytes_to_int(4)
            _mask = Mask(x, y, w, h)
            _mask.size = size
            _mask.file_pos = self.hand.tell()

            i = y // 240 - (y % 240 == 0)
            j = x // 320 - (x % 320 == 0)
            ii = (y + h) // 240 - ((y + h) % 240 == 0)
            jj = (x + w) // 320 - ((x + w) % 320 == 0)
            for _i in range(i, ii+1):
                for _j in range(j, jj+1):
                    unit_num = _i * self.col + _j
                    self.mask[unit_num].append(_mask)

    def _read_bytes_to_int_list(self, size):
        return [x for x in self.hand.read(size)]

    def _read_bytes_to_hex_list(self, size):
        hex_bit = binascii.hexlify(self.hand.read(size)).decode("utf-8")
        return [hex_bit[i:i+2] for i in range(0, len(hex_bit), 2)]

    def _read_bytes_to_int(self, size):
        return int.from_bytes(self.hand.read(size), byteorder="little", signed=True)

    @staticmethod
    def _repair_new_jpg(pic):
        i = 0
        while i < len(pic):
            if pic[i:i + 2] == ['ff', 'd8']:  # 过
                i += 2
            elif pic[i:i + 2] == ['ff', 'a0']:  # 删除第3、4个字节 FFA0
                del pic[i:i + 2]
            elif pic[i:i + 2] == ['ff', 'c0']:  # 过
                i += 2
                i += int(pic[i] + pic[i + 1], 16)
            elif pic[i:i + 2] == ['ff', 'c4']:  # 过
                i += 2
                i += int(pic[i] + pic[i + 1], 16)
            elif pic[i:i + 2] == ['ff', 'db']:  # 过
                i += 2
                i += int(pic[i] + pic[i + 1], 16)
            elif pic[i:i + 2] == ['ff', 'da']:  #
                i += 2
                da_len = int(pic[i] + pic[i + 1], 16)
                pic[i:i + 2] = ['00', '0c']  # 修改FF DA的长度00 09 为 00 0C
                i += da_len
                for x in ["00", "3f", "00"]:  # 在FF DA数据的最后添加00 3F 00
                    pic.insert(i, x)
                    i += 1
                while i < len(pic):  # 替换FF DA到FF D9之间的FF数据为FF 00
                    if pic[i] == "ff":
                        pic.insert(i + 1, "00")
                        i += 1
                    i += 1
                pic = pic[:-2] + ["d9"]  # 但结束标志ff d9 不能改 // 这里多了一个字节，所以减去。
            else:
                break
        return pic

    @staticmethod
    def _hex_list_to_bytes(_list):
        _bytes = bytes()
        for i in _list:
            _bytes += int(i, 16).to_bytes(length=1, byteorder='big')
        return _bytes


simple_old_map = MapX("scene/0001.map")