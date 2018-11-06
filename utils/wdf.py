# -*- coding: utf-8 -*-
import binascii

from utils.xy2_res import read_color_palette, read_pic
from settings import XY2PATH

"""
WDF --> WdfFile --> WAS
"""


class WDF:
    """
    WDF文件读取类
    """
    def __init__(self, name):
        self.name = name
        self.path = XY2PATH + name
        self.hand = None
        self.flag = None  # 文件标签50，46，44，57
        self.n = 0
        self.offset = 0
        self.file_dict = {}
        self._open()
        self._get_file_list()

    def _open(self):
        """
        读取WDF文件头
        :return:
        """
        try:
            self.hand = open(self.path, 'rb')
        except FileNotFoundError:
            raise Exception("找不到{}文件".format(self.path))
        else:
            self.flag = self.read_bytes_to_hex_list(4)  # WDF包裹文件标志
            if self.flag != ['50', '46', '44', '57']:
                raise Exception("WDF文件类型错误，{}".format(self.path))
            self.n = self.read_bytes_to_int(4)  # WDF包裹内文件数量
            self.offset = self.read_bytes_to_int(4)  # 文件列表偏移地址

    def _get_file_list(self):
        """
        读取WDF内的文件列表，每一个wdf_file，指向一个was
        :return:
        """
        self.hand.seek(self.offset)
        for i in range(self.n):
            _hash = self.get_hash(4)
            offset = self.read_bytes_to_int(4)
            size = self.read_bytes_to_int(4)
            spaces = self.read_bytes_to_int(4)
            wdf_file = WDFUnit(_hash, offset, size, spaces)
            self.file_dict[_hash] = wdf_file

    def get(self, _hash):
        """
        根据已读取的文件列表和_hash，读取WAS
        :param _hash:
        :return:
        """
        wdf_unit = self.file_dict[_hash]
        self.hand.seek(wdf_unit.offset)
        flag = self.read_bytes_to_hex_list(2)
        if flag == ['53', '50']:
            return WAS(wdf_unit.offset, self.hand)
        elif flag == ["ff", "d8"]:
            return JPG(wdf_unit, self.hand)
        elif flag == ["00", "00"]:
            return TGA(wdf_unit, self.hand)
        elif flag == ['50', '20']:
            return Chat(wdf_unit, self.hand)
        print(flag)

    def read_bytes_to_hex_list(self, size):
        hex_bit = binascii.hexlify(self.hand.read(size)).decode("utf-8")
        return [hex_bit[i:i+2] for i in range(0, len(hex_bit), 2)]

    def get_hash(self, size):
        return "0x" + "".join(self.read_bytes_to_hex_list(size)[::-1]).upper()

    def read_bytes_to_int(self, size):
        return int("".join(self.read_bytes_to_hex_list(size)[::-1]), 16)


class WDFUnit:
    """
    WDF内部的文件列表
    """
    def __init__(self, _hash, offset, size, spaces):
        self.hash = _hash
        self.offset = offset
        self.size = size
        self.spaces = spaces


class WAS:
    def __init__(self, offset, hand):
        self.offset = offset  # 文件初始位置
        self.hand = hand  # 文件操作
        self.type = "WAS"
        self.flag = []  # 文件标记 2byte
        self.head_size = 0  # 文件头长度 2byte，不包括这4字节
        self.direction_num = 0  # 动画图片的方向数 2byte
        self.direction_pic_num = 0  # 每一方向的图片数量 2byte
        self.width = 0  # 动画总宽度 2byte
        self.height = 0  # 动画总高度 2byte
        self.size = None
        self.x = 0  # 动画关键点 X 2byte
        self.y = 0  # 动画关键点 Y 2byte
        self.other = None
        self.color_board = None  # 512bytes 调色板
        self.color_board_origin = None
        self.pic = []
        self._open()  # 读取WAS头
        self._read_color_board()  # 读取调色板
        self.pic_offsets = [self.read_bytes_to_int(4) + self.offset + 4 + self.head_size
                            for _ in range(self.direction_num * self.direction_pic_num)]  # WAS内图片的偏移地址4bytes
        self._get_frames()

    def _open(self):
        """
        读取WAS文件头
        :return:
        """
        self.hand.seek(self.offset)  # 跳转到WAS对应的位置
        self.flag = self.read_bytes_to_hex_list(2)  # WAS标志SP
        if self.flag != ['53', '50']:  # "SP"
            raise Exception("WAS文件错误")
        self.head_size = self.read_bytes_to_int(2)
        self.direction_num = self.read_bytes_to_int(2)
        self.direction_pic_num = self.read_bytes_to_int(2)
        self.width = self.read_bytes_to_int(2)
        self.height = self.read_bytes_to_int(2)
        self.size = (self.width, self.height)
        self.x = self.read_bytes_to_int(2)
        self.y = self.read_bytes_to_int(2)
        # TODO
        if self.head_size > 12:  # 如果不是12，可能包含其他信息，如帧停留时间
            self.other = self.hand.read(self.head_size - 12)
            print(self.other)
            print(self.direction_num)
            print(self.direction_pic_num)

    def _read_color_board(self):
        """
        读取调色板
        :return:
        """
        self.color_board_origin = self.hand.read(512)  # 原始的RGB565数据
        self.color_board = read_color_palette(self.color_board_origin)

    def _get_frames(self):
        """
        获取was内每一帧图片
        :return:
        """
        temp_size = 0
        for i in range(len(self.pic_offsets)):
            if i < len(self.pic_offsets) - 1:
                temp_size = self.pic_offsets[i+1] - self.pic_offsets[i]
            else:
                temp_size += 1000  # 由于最后一个大小方便确定，为保证数据完整，多读1000字节
            self.hand.seek(self.pic_offsets[i])
            data = self.hand.read(temp_size)  # 先获取pic data
            _pic = Frame(self.pic_offsets[i], self.hand)
            _pic.data = read_pic(data, _pic, self.color_board_origin, self.color_board)  # 利用dll解析每一帧图片
            self.pic.append(_pic)

    def read_bytes_to_hex_list(self, size):
        hex_bit = binascii.hexlify(self.hand.read(size)).decode("utf-8")
        return [hex_bit[i:i + 2] for i in range(0, len(hex_bit), 2)]

    def read_bytes_to_int(self, size):
        return int.from_bytes(self.hand.read(size), byteorder="little", signed=True)


class Frame:
    def __init__(self, offset, hand):
        self.offset = offset
        self.hand = hand
        self.x = 0  # 关键点 X
        self.y = 0  # 关键点 Y
        self.width = 0  # 图片宽度
        self.height = 0  # 图片高度
        self.data = None
        self._open()

    def _open(self):
        self.hand.seek(self.offset)
        self.x = self.read_bytes_to_int(4)
        self.y = self.read_bytes_to_int(4)
        self.width = self.read_bytes_to_int(4)
        self.height = self.read_bytes_to_int(4)

    def read_bytes_to_int(self, size):
        return int.from_bytes(self.hand.read(size), byteorder="little", signed=True)


class JPG:
    def __init__(self, wdf_unit, hand):
        self.type = "JPG"
        self.offset = wdf_unit.offset
        self.size = wdf_unit.size
        self.spaces = wdf_unit.spaces
        self.hand = hand
        self.hand.seek(self.offset)
        self.data = self.hand.read(self.size)


class TGA:
    def __init__(self, wdf_unit, hand):
        self.type = "TGA"
        self.offset = wdf_unit.offset
        self.size = wdf_unit.size
        self.spaces = wdf_unit.spaces
        self.hand = hand
        self.hand.seek(self.offset)
        self.data = self.hand.read(self.size)


class Chat:
    def __init__(self, wdf_unit, hand):
        self.type = "Chat"
        self.offset = wdf_unit.offset
        self.size = wdf_unit.size
        self.spaces = wdf_unit.spaces
        self.hand = hand
        self.hand.seek(self.offset)
        self.data = self.hand.read(self.size)
        self.chats = []
        self.read_chat()

    def read_chat(self):
        chats = self.data.split(b"\x50\x20\x4e\x0d\x0a")[1:]
        for c in chats:
            self.chats.append(c.decode("gbk"))


class PicPy:    # 用Python去解析帧图片，该方法过慢，已经弃用，保留仅供阅读
    def __init__(self, offset, hand, cb, cbr):
        self.offset = offset
        self.hand = hand
        self.x = 0  # 关键点 X
        self.y = 0  # 关键点 Y
        self.width = 0  # 图片宽度
        self.height = 0  # 图片高度
        self.data = None
        self.color_board = cb
        self.color_board_origin = cbr
        self._open()
        self.row_offset = [self.read_bytes_to_int(4) + self.offset for _ in range(self.height)]  # 行偏移量列表
        self.data = self._read_row()

    def _open(self):
        self.hand.seek(self.offset)
        self.x = self.read_bytes_to_int(4)
        self.y = self.read_bytes_to_int(4)
        self.width = self.read_bytes_to_int(4)
        self.height = self.read_bytes_to_int(4)

    def read_bytes_to_hex_list(self, size):
        hex_bit = binascii.hexlify(self.hand.read(size)).decode("utf-8")
        return [hex_bit[i:i + 2] for i in range(0, len(hex_bit), 2)]

    def read_bytes_to_int(self, size):
        return int("".join(self.read_bytes_to_hex_list(size)[::-1]), 16)

    def _read_row(self):
        data = bytes()
        for pos in self.row_offset:
            self.hand.seek(pos)
            one_row = bytes()  # 一行ARGB数据
            pixel_num = 0
            while True:
                _type = self.read_bytes_to_bin(1)
                if _type[:2] == "00":
                    if _type == "00000000":  # 该行结束
                        if pixel_num < self.width:
                            rgba = int(0).to_bytes(length=4, byteorder='little')
                            for _ in range(self.width - pixel_num):
                                one_row += rgba
                        break
                    if _type[2] == "1":  # 若第3个比特为1,则剩下的5个比特为alpha值
                        alpha = int(_type[3:], 2)
                        if pixel_num < self.width:
                            rgba = self.mix_rgb_565(alpha)
                            one_row += rgba
                            pixel_num += 1
                        else:
                            break
                    else:  # 若第3个比特为0 则表示将要重复alpha像素,剩下的5个比特为重复的次数
                        n = int(_type[3:], 2)
                        alpha = self.read_bytes_to_int(1)  # 1 byte
                        rgba = self.mix_rgb_565(alpha)
                        flag = True
                        for _ in range(n):
                            if pixel_num < self.width:
                                one_row += rgba
                                pixel_num += 1
                            else:
                                flag = False
                                break
                        if not flag:
                            break
                elif _type[:2] == "01":  # 普通像素，剩下的6个比特表示数据段的长度,之后长度个字节的调色板索引
                    n = int(_type[2:], 2)
                    alpha = int(255).to_bytes(length=1, byteorder='little')
                    flag = True
                    for _ in range(n):
                        if pixel_num < self.width:
                            rgb = self.from_color_board_get_rgb()
                            one_row += rgb + alpha
                            pixel_num += 1
                        else:
                            flag = False
                            break
                    if not flag:
                        break
                elif _type[:2] == "10":  # 重复像素，剩下的6个比特为重复的次数，之后的一个字节为调色板索引
                    n = int(_type[2:], 2)
                    alpha = int(255).to_bytes(length=1, byteorder='little')
                    rgb = self.from_color_board_get_rgb()
                    flag = True
                    for _ in range(n):
                        if pixel_num < self.width:
                            one_row += rgb + alpha
                            pixel_num += 1
                        else:
                            flag = False
                            break
                    if not flag:
                        break
                else:  # 跳过像素，剩下的6个比特表示跳过像素的数量
                    n = int(_type[2:], 2)
                    rgba = int(0).to_bytes(length=4, byteorder='little')
                    flag = True
                    for _ in range(n):
                        if pixel_num < self.width:
                            one_row += rgba
                            pixel_num += 1
                        else:
                            flag = False
                            break
                    if not flag:
                        break
            data += one_row
        return data

    def read_bytes_to_bin(self, size):
        temp = bin(int.from_bytes(self.hand.read(size), byteorder="big"))[2:]
        prefix = "0" * (8 - len(temp))
        return prefix + temp

    def from_color_board_get_rgb(self):
        n = self.read_bytes_to_int(1) * 3
        return self.color_board[n:n+3]

    def mix_rgb_565(self, alpha):
        n = self.read_bytes_to_int(1) * 2
        rgb_565 = int.from_bytes(self.color_board_origin[n:n+2], byteorder='little')
        alpha_pixel = self.alpha_565(rgb_565, 0, alpha)
        argb = self.rgb_565_to_argb_8888(alpha_pixel, alpha*8)
        return argb

    @staticmethod
    def alpha_565(src, des, alpha):
        r_src = (src & 0xf800) >> 11
        g_src = (src & 0x07e0) >> 5
        b_src = src & 0x001f

        r_des = (des & 0xf800) >> 11
        g_des = (des & 0x07e0) >> 5
        b_des = des & 0x001f

        r = ((r_src - r_des) * alpha) >> 5 + r_des
        g = ((g_src - g_des) * alpha) >> 5 + g_des
        b = ((b_src - b_des) * alpha) >> 5 + b_des
        return (r << 11) | (g << 5) | b

    @staticmethod
    def rgb_565_to_argb_8888(rgb_565, alpha):
        r = (rgb_565 >> 11) & 0x1f
        g = (rgb_565 >> 5) & 0x3f
        b = rgb_565 & 0x1f

        r = (r << 3) | (r >> 2)
        g = (g << 2) | (g >> 4)
        b = (b << 3) | (b >> 2)

        _bytes = r.to_bytes(length=1, byteorder='little')
        _bytes += g.to_bytes(length=1, byteorder='little')
        _bytes += b.to_bytes(length=1, byteorder='little')
        _bytes += alpha.to_bytes(length=1, byteorder='little')
        return _bytes
