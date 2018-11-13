from core.state.state import State
from utils.math import quest_25, quest_16

import logging
log = logging.getLogger('')


class MapState(State):
    portals = []

    def early_update(self, data):
        units_needed = quest_25(self.game_object.window, self.game_object.row, self.game_object.col)
        for i in units_needed:
            if not self.game_object.unit_has_blitted[i]:  # 如果该单元还没有数据
                if self.game_object.quest_timer[i] == 0:  # 且该单元还没有发送过请求
                    self.game_object.map_client.request_map_unit(self.game_object.map_id, unit_num=i)
                self.game_object.quest_timer[i] = +1
                if self.game_object.quest_timer[i] == 5:  # 累计请求5次后重置为0
                    self.game_object.quest_timer[i] = 0

    def update(self, data):
        super().update(data)
        no_repeat = {}
        masks = []
        self.portals = []
        units = quest_16(self.game_object.window, self.game_object.row, self.game_object.col,
                         width_margin=60, height_margin=40)
        flag = True
        for i in units:
            if not self.game_object.unit_has_blitted[i]:
                flag = False
            for mask in self.game_object.masks_of_unit[i]:
                if (mask.rect.x, mask.rect.y) not in no_repeat:
                    no_repeat[(mask.rect.x, mask.rect.y)] = True
                    masks.append(mask)
            self.portals += self.game_object.portals_of_unit[i]
        self.game_object.ready = flag
        data["portals"] = self.portals
        data["other_masks"] = masks
        data["left_top"] = self.game_object.get_left_top()
        data["collision_window"] = self.game_object.get_collision_window()

    def late_update(self, data=None):
        self.game_object.set_window(data["me_world_pc"])
        self.game_object.me_world_pc = data["me_world_pc"]
        for portal in self.portals:
            portal.update(data)

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.game_object.surface, (0, 0), self.game_object.window)
        for portal in self.portals:
            portal.draw(screen)

    def enter(self):
        log.debug("初始化地图")
