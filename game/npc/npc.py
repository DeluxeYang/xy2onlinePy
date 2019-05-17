import pygame
from pygame.locals import *

from core.entity.game_object import GameObject

from game.npc.npc_state import NPCState


class NPC(GameObject):
    def __init__(self, npc_name, npc_id, npc_type,
                 res_info, direction,
                 map_version, map_id, x, y):
        super().__init__(x, y)

        self.npc_name = npc_name
        self.npc_id = npc_id
        self.npc_type = npc_type

        self.map_version = map_version
        self.map_id = map_id

        self.screen_rect = Rect((0, 0), (0, 0))

        self.res_info = res_info
        self.direction = direction

        self.is_mouse_over = False

        self.init_state(NPCState())
