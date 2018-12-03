from core.entity.game_object import GameObject
from core.state.static_state import StaticState


class StaticObject(GameObject):
    def __init__(self, res_info, x, y, z=0):
        super().__init__(x, y, z)
        self.res_info = res_info
        self.direction = 0
        self.inited = True
        self.ready = True


def static_object_factory(res_info, x, y, z=0):
    obj = StaticObject(res_info, x, y, z)
    obj.init_state(StaticState())
    return obj
