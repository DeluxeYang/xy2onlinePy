from core.entity.game_object import GameObject
from core.state.material_animation_state import MaterialAnimationState


class MaterialAnimationObject(GameObject):
    def __init__(self, res_info, x, y, z=0):
        super().__init__(x, y, z)
        self.res_info = res_info
        self.direction = 0
        self.inited = True
        self.ready = True


def material_animation_object_factory(res_info, x, y, z=0):
    obj = MaterialAnimationObject(res_info, x, y, z)
    obj.init_state(MaterialAnimationState())
    return obj
