import pygame
from pygame.locals import *
from PIL import Image
from io import BytesIO
from settings import Res_Margin
from utils.wdf import WDF
from utils.mask import Mask


class WAS:
    """
    WAS动画管理类，存储各个方向的帧图片和帧mask
    """
    def __init__(self, direction_num, frame_num, x, y, w, h):
        self.image_group = []
        self.mask_group = []
        self.direction_num = direction_num
        self.frame_num = frame_num
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class ResManager:
    """
    WDF资源管理类，单例，WDF缓存
    """
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.wdf_pool = {}
        self.was_pool = {}

    def get_res(self, wdf_name, _hash, with_mask=True):
        """
        获得WDF资源
        :param wdf_name: wdf 文件名
        :param _hash:  hash值
        :param with_mask:  是否生成对应的mask
        :return:
        """
        if wdf_name not in self.wdf_pool:  # 该实例为单例模式，并且将所有已读取的wdf资源缓存
            self.wdf_pool[wdf_name] = WDF(wdf_name)
        _wdf = self.wdf_pool[wdf_name]  # wdf
        _instance = _wdf.get(_hash)  # was tga jpg 等
        res = None
        if _instance.type == "WAS":
            if (wdf_name, _hash) in self.was_pool:
                return self.was_pool[(wdf_name, _hash)]
            res = WAS(_instance.direction_num, _instance.direction_pic_num,
                      _instance.x, _instance.y, _instance.width, _instance.height)  # Res资源实例
            self.was_pool[(wdf_name, _hash)] = res
            for i in range(_instance.direction_num):
                _surface = []
                _mask = []
                rect = Rect(0, 0, 0, 0)
                for j in range(_instance.direction_pic_num):
                    pic = _instance.pic[i * _instance.direction_pic_num + j]
                    image = pygame.Surface((_instance.width+Res_Margin*2,
                                            _instance.height+Res_Margin*2), pygame.SRCALPHA)
                    im = pygame.image.frombuffer(pic.data, (pic.width, pic.height), "RGBA").convert_alpha()
                    position = (_instance.x+Res_Margin - pic.x, _instance.y+Res_Margin - pic.y)  # was关键点 - 帧图片关键点
                    image.blit(im, position)
                    _surface.append(image)
                    if with_mask:
                        py_mask = pygame.mask.from_surface(image)  # 生成该was的mask
                        _mask.append(Mask(rect, py_mask))
                res.image_group.append(_surface)
                if with_mask:
                    res.mask_group.append(_mask)
        elif _instance.type == "JPG":
            jpg_file = BytesIO(_instance.data)
            res = pygame.image.load(jpg_file).convert()
        elif _instance.type == "TGA":
            tga_file = BytesIO(_instance.data)
            temp = Image.open(tga_file)
            res = pygame.image.frombuffer(temp.tobytes(encoder_name='raw'), temp.size, "RGBA")
        elif _instance.type == "Chat":
            print(_instance.chats)
        return res


res_manager = ResManager()