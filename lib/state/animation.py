import pygame
from pygame.locals import *

from .state import State
from utils.res_manager import res_manager
from settings import ResMargin

bright = pygame.Surface((400, 400), flags=pygame.SRCALPHA)
bright.fill((80, 80, 80, 0))


class AnimationState(State):
    """
    WDF动画+状态
    """
    res_index = ""

    def __init__(self):
        super().__init__()
        self.res = None
        self.surface = None
        self.frame = 0
        self.first_frame = 0
        self.last_frame = 0
        self.last_time = 0
        self.old_frame = 0
        self.is_forward = True

    def register(self, obj):
        """
        绑定GameObject
        :param obj:
        :return:
        """
        self.game_object = obj
        address = self.game_object.res_info[self.res_index]
        self.res = res_manager.get_res(address[0], address[1])  # 找到动画资源
        self.last_frame = self.res.frame_num
        self.game_object.inited = True  # 初始化完成

    def _update(self, data):
        one_loop = self.calc_next_frame(data["current_time"], rate=100)  # 计算下一帧的帧数
        self.set_surface(self.game_object.direction, data["other_masks"], self.game_object.get_xy())  # 设定surface
        self.game_object.mask = self.get_mask(self.game_object.direction)  # 设定shape对应的mask
        self.game_object.ready = True
        self.game_object.screen_rect = self.get_screen_rect(data["left_top"])  # 根据shape的World 坐标和left_top，确定相对屏幕坐标
        return one_loop

    def draw(self, _screen, highlight=False):
        """
        动画绘制到屏幕上
        :param _screen:
        :param highlight:
        :return:
        """
        surface = self.surface.copy()
        if highlight:
            surface.blit(bright, (0, 0), special_flags=BLEND_RGB_ADD)
        _screen.blit(surface, self.game_object.screen_rect)

    def get_mask(self, direction):
        return self.res.mask_group[direction][self.frame]

    def calc_next_frame(self, current_time, rate):
        """
        计算是否移动到下一帧
        :param current_time:
        :param rate:
        :return:
        """
        one_loop = False
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame >= self.last_frame:
                self.frame = self.first_frame
                one_loop = True  # 一次动画循环完毕
            self.last_time = current_time
        return one_loop

    def set_surface(self, direction, other_masks=None, world_pc=None):
        """
        设置surface
        :param direction:
        :param other_masks:  其他Mask，如果传入则需进行遮挡处理
        :param world_pc:  Mask遮挡判断时所需的世界像素坐标
        :return:
        """
        if self.frame != self.old_frame:
            if other_masks:
                self.surface = self.get_image_under_mask(direction, other_masks, world_pc)
            else:
                self.surface = self.get_image(direction)
            self.old_frame = self.frame

    def get_image(self, direction):
        """
        直接取得帧图片
        :param direction:
        :return:
        """
        return self.res.image_group[direction][self.frame]

    def get_image_under_mask(self, direction, other_masks, world_pc):
        """
        检测该动画帧图片与地形mask是否碰撞，然后返回经过部分半透明处理的帧图片
        :param other_masks:  地图MASK
        :param world_pc: 动画的地图坐标
        :param direction:
        :return:
        """
        sprite_surface = self.res.image_group[direction][self.frame].copy()
        sprite_map_x = int(world_pc[0]) - ResMargin - self.res.x
        sprite_map_y = int(world_pc[1]) - ResMargin - self.res.y
        sprite_mask = self.res.mask_group[direction][self.frame].mask
        sprite_array = pygame.surfarray.pixels_alpha(sprite_surface)  # 像素透明度Array
        for mask in other_masks:
            offset_x = mask.rect.x - sprite_map_x
            offset_y = mask.rect.y - sprite_map_y
            if mask.collision_mask and sprite_mask.overlap(mask.collision_mask, (offset_x, offset_y)):
                continue  # 如果和collision_mask重叠, 则判定角色在mask前面，不产生遮挡，跳过
            alpha = 127
            overlap = sprite_mask.overlap(mask.mask, (offset_x, offset_y))
            if overlap:  # 如果遮挡
                width, height = sprite_mask.get_size()
                w, h = mask.mask.get_size()
                for y in range(height):  # 循环检测遮挡点
                    for x in range(width):
                        if sprite_mask.get_at((x, y)) and (
                                                0 <= x - offset_x < w and 0 <= y - offset_y < h
                                and mask.mask.get_at((x - offset_x, y - offset_y))):
                            sprite_array[x, y] = alpha
        del sprite_array  # 必须删除，释放掉array才能解锁surface
        return sprite_surface

    def get_world_rect(self):
        x = int(self.game_object.x) - ResMargin - self.res.x
        y = int(self.game_object.y) - ResMargin - self.res.y
        w = self.res.w
        h = self.res.h
        return Rect(x, y, w, h)

    def get_screen_rect(self, left_top):
        world_rect = self.get_world_rect()
        return world_rect.move(-left_top[0], -left_top[1])
