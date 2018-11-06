from .state import State
from utils.math import quest_16


class MapState(State):
    def update(self, data=None):
        no_repeat = {}
        masks = []
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
        self.game_object.ready = flag
        data["other_masks"] = masks
        data["left_top"] = self.game_object.get_left_top()
        data["collision_window"] = self.game_object.get_collision_window()

    def draw(self, screen):
        screen.blit(self.game_object.surface, (0, 0), self.game_object.window)
