import pygame
from pygame.locals import *
from utils.res_manager import res_manager
from settings import Res_Margin

bright = pygame.Surface((400, 400), flags=pygame.SRCALPHA)
bright.fill((80, 80, 80, 0))


class Animation:
    """
    WDF动画渲染类
    """
    def __init__(self, address):
        self.res = res_manager.get_res(address[0], address[1])
        self.image = None
        self.frame = 0
        self.first_frame = 0
        self.last_frame = self.res.frame_num
        self.last_time = 0
        self.old_frame = 0
        self.is_forward = True

    def draw(self, window_rect, highlight=False):
        """
        动画绘制到屏幕上
        :param window_rect:
        :param highlight:
        :return:
        """
        image = self.image.copy()
        if highlight:
            image.blit(bright, (0, 0), special_flags=BLEND_RGB_ADD)
        _screen = pygame.display.get_surface()
        _screen.blit(image, window_rect)

    def get_mask(self, direction):
        return self.res.mask_group[direction][self.frame]

    def _cal_next_frame(self, current_time, rate):
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

    def _render(self, direction, other_masks=None, world_pc=None):
        """
        将帧图片渲染到image上
        :param direction:
        :param other_masks:
        :param world_pc:
        :return:
        """
        if self.frame != self.old_frame:
            if other_masks:
                self.image = self._get_image_under_mask(direction, other_masks, world_pc)
            else:
                self.image = self._get_image(direction)
            self.old_frame = self.frame

    def _get_image(self, direction):
        """
        直接取得帧图片
        :param direction:
        :return:
        """
        return self.res.image_group[direction][self.frame]

    def _get_image_under_mask(self, direction, other_masks, world_pc):
        """
        检测该动画帧图片与地形mask是否碰撞，然后返回经过部分半透明处理的帧图片
        :param other_masks:  地图MASK
        :param world_pc: 动画的地图坐标
        :param direction:
        :return:
        """
        sprite_surface = self.res.image_group[direction][self.frame].copy()
        sprite_map_x = int(world_pc[0]) - Res_Margin - self.res.x
        sprite_map_y = int(world_pc[1]) - Res_Margin - self.res.y
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

    def _cal_next_frame_in_loop(self, current_time, rate):
        """
        动画帧来回更新, 计算是否移动到下一帧
        :param current_time:
        :param rate:
        :return:
        """
        one_loop = False
        if current_time > self.last_time + rate:
            if self.is_forward:
                self.frame += 1
                if self.frame >= self.last_frame:
                    self.frame = self.last_frame - 1
                    self.is_forward = False
            else:
                self.frame -= 1
                if self.frame <= self.first_frame:
                    self.is_forward = True
                    one_loop = True
            self.last_time = current_time
        return one_loop
