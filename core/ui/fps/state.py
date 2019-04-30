from core.ui.state.static_ui_state import StaticUIState
import pygame
from core.world.director import director


class FPSState(StaticUIState):
    res_index = "normal"

    def update(self, context):
        super().update(context)
        self.game_object.text = "FPS: " + str(int(director.clock.get_fps()))
        self.game_object.text_field.update_text(self.game_object.text)



