from pygame.locals import *

from core.state.animation_state import AnimationState
from core.entity.game_object import GameObject


class Portal(GameObject):
    def __init__(self, position, target_map_id, target_position, show=False, wdf=None, _hash=None):
        super().__init__()
        self.x = position[0]
        self.y = position[1]
        self.portal_rect = Rect((self.x-10, self.y-10), (20, 20))

        self.target_map_id = target_map_id
        self.target_position = target_position

        self.direction = 0
        self.is_show = show
        self.res_info = {"portal": [wdf, _hash]}

        self.mask = None
        self.screen_rect = None


class PortalState(AnimationState):
    res_index = "portal"

    def draw(self, _screen, highlight=False):
        _screen.blit(self.game_object.surface, self.game_object.screen_rect)


def portal_factory(position, target_map_id, target_position, show=False, wdf=None, _hash=None):
    portal = Portal(position, target_map_id, target_position, show, wdf, _hash)
    if show:
        portal_state = PortalState()
        portal.init_state(portal_state)
    return portal