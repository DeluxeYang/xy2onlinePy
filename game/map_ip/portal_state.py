from core.state.material_animation_state import MaterialAnimationState
from core.world.director import director


class PortalState(MaterialAnimationState):
    def update(self, context):
        super().update(context)

        if self.game_object.rect.collidepoint(director.account.get_main_role().get_xy()):
            print("ININININININIn")
