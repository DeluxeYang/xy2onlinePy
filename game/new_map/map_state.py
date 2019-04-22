from core.world.director import director

from core.state.state import State
from utils.math import quest_25, quest_16

import logging
log = logging.getLogger('')


class MapState(State):
    units_needed = []

    def early_update(self, context):
        """
        预先请求地图数据
        :param context:
        :return:
        """
        self.units_needed = quest_16(self.game_object.window, self.game_object.row, self.game_object.col)
        for i in self.units_needed:
            if not self.game_object.unit_has_blitted[i]:  # 如果该单元还没有数据
                pass

    def update(self, context):
        """
        地图更新，主要作用为获取地图mask、left_top、碰撞窗口，为shape层使用
        :param context:
        :return:
        """
        super().update(context)
        no_repeat = {}
        masks = []
        for i in self.units_needed:
            for mask in self.game_object.mask_of_unit[i]:
                if (mask.rect.x, mask.rect.y) not in no_repeat:
                    no_repeat[(mask.rect.x, mask.rect.y)] = True
                    masks.append(mask)
        context["map_masks"] = masks
        context["left_top"] = self.game_object.get_left_top()
        context["collision_window"] = self.game_object.get_collision_window()

    def late_update(self, context=None):
        """
        shape层更新后，map视图更新
        :param context:
        :return:
        """
        main_role = director.account.get_main_role()  # main_role
        self.game_object.set_window(main_role.get_pc())  # 根据主要角色设置地图范围

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.game_object.surface, (0, 0), self.game_object.window)

    def enter(self):
        log.debug("初始化地图")
