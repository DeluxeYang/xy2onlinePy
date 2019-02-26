from core.ui.state.static_ui_state import StaticUIState
from core.ui.state.animated_ui_state import AnimatedUIState
from settings import ResMargin, logger


class FrameState(StaticUIState):
    res_index = "normal"


class AnimatedFrameState(AnimatedUIState):
    res_index = "normal"

    def update(self, context):
        if self.game_object.res_info:
            super().update(context)

    def draw(self, screen):
        w, h = self.game_object.surface.get_size()
        temp_rect = self.game_object.screen_rect.move(
            -((w-self.game_object.w)//2), -((h-self.game_object.h)//2))
        screen.blit(self.game_object.surface, temp_rect)
