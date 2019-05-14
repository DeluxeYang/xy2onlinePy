import numpy
import pygame
from pygame.locals import Rect
from io import BytesIO

from core.world.director import director
from utils.mask import Mask
from core.state.state import State
from utils.math import quest_16

from settings import logger


class MapState(State):
    ready = False

    def early_update(self, context):
        """
        预先请求地图数据
        :param context:
        :return:
        """
        flag = True
        units_needed = quest_16(self.game_object.window, self.game_object.map_x.row, self.game_object.map_x.col)
        for i in units_needed:
            if not self.game_object.unit_has_blitted[i]:  # 如果该单元还没有数据
                flag = False
                jpeg, masks_data = self.game_object.map_x.read_unit(i)
                self._blit_unit(jpeg, i)
                self.game_object.masks_of_unit[i] = []
                for mask_data in masks_data:
                    try:
                        self.game_object.masks_of_unit[i].append(self._generate_mask(mask_data))  # 生成Mask
                    except Exception as e:
                        logger.error("Map Mask Error" + str(self.game_object.map_id) + " " + str(i) + str(e))
                self.game_object.unit_has_blitted[i] = True
                break
        self.ready = self.ready or flag
        self.game_object.ready = self.ready

    def update(self, context):
        """
        地图更新，主要作用为获取地图mask、left_top、碰撞窗口，为shape层使用
        :param context:
        :return:
        """
        super().update(context)
        no_repeat = {}
        masks = []
        units = quest_16(self.game_object.window, self.game_object.map_x.row, self.game_object.map_x.col,
                         width_margin=60, height_margin=40)
        for i in units:
            for mask in self.game_object.masks_of_unit[i]:
                if (mask.rect.x, mask.rect.y) not in no_repeat:
                    no_repeat[(mask.rect.x, mask.rect.y)] = True
                    masks.append(mask)
        context["other_masks"] = masks
        context["left_top"] = self.game_object.get_left_top()
        context["collision_window"] = self.game_object.get_collision_window()

    def late_update(self, context=None):
        """
        shape层更新后，map视图更新
        :param context:
        :return:
        """
        main_role = director.account.get_main_role()  # main_role
        self.game_object.set_window(main_role.get_xy())  # 根据主要角色设置地图范围

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.game_object.surface, (0, 0), self.game_object.window)

    def enter(self):
        logger.debug("初始化地图")

    def _blit_unit(self, jpg, unit_num):
        """
        将单元图片blit到MAP上
        :param jpg:
        :param unit_num:
        :return:
        """
        self.game_object.unit_has_blitted[unit_num] = True
        if self.game_object.map_x.map_type == 1:
            unit_image = pygame.image.frombuffer(jpg, (320, 240), "RGB")
        else:
            jpg_file = BytesIO(jpg)
            unit_image = pygame.image.load(jpg_file).convert()
        row = unit_num // self.game_object.map_x.col  # 行号
        col = unit_num % self.game_object.map_x.col  # 列号
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
