from core.world.director import director

from core.state.state import State
from utils.math import quest_25, quest_16

import logging
log = logging.getLogger('')


class MapState(State):
    def early_update(self, context):
        """
        预先请求地图数据
        :param context:
        :return:
        """
        units_needed = quest_16(self.game_object.window, self.game_object.row, self.game_object.col)
        for i in units_needed:
            if not self.game_object.unit_has_blitted[i]:  # 如果该单元还没有数据
                if self.game_object.quest_timer[i] == 0:  # 且该单元还没有发送过请求
                    self.game_object.map_client.request_map_unit(self.game_object.map_id, unit_num=i)
                self.game_object.quest_timer[i] = +1
                if self.game_object.quest_timer[i] == 5:  # 累计请求5次后重置为0
                    self.game_object.quest_timer[i] = 0

    def update(self, context):
        """
        地图更新，主要作用为获取地图mask、left_top、碰撞窗口，为shape层使用
        :param context:
        :return:
        """
        super().update(context)
        no_repeat = {}
        masks = []
        units = quest_16(self.game_object.window, self.game_object.row, self.game_object.col,
                         width_margin=60, height_margin=40)
        flag = True
        for i in units:
            # if not self.game_object.unit_has_blitted[i]:
            #     flag = False
            for mask in self.game_object.masks_of_unit[i]:
                if (mask.rect.x, mask.rect.y) not in no_repeat:
                    no_repeat[(mask.rect.x, mask.rect.y)] = True
                    masks.append(mask)
        self.game_object.ready = flag
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
        self.game_object.set_window(main_role.get_pc())  # 根据主要角色设置地图范围

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.game_object.surface, (0, 0), self.game_object.window)

    def enter(self):
        log.debug("初始化地图")
