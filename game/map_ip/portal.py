from pygame.locals import *
from core.entity.material_animation_object import MaterialAnimationObject
from game.map_ip.portal_state import PortalState


class Portal(MaterialAnimationObject):
    def __init__(self, res_info, map_version, map_id, x, y,
                 target_map_version, target_map_id, target_x, target_y):
        super().__init__(res_info, x, y)

        self.map_version = map_version
        self.map_id = map_id

        self.target_map_version = target_map_version
        self.target_map_id = target_map_id
        self.target_x = target_x
        self.target_y = target_y

        self.rect = Rect(x - 20, y - 20, 40, 40)

        self.init_state(PortalState())
