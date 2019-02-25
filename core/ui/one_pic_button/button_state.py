import pygame
from core.ui.state.animated_ui_state import AnimatedUIState
from core.ui.state.static_ui_state import StaticUIState
from core.ui.state.ui_state import UIState


class ButtonNormalState(StaticUIState):
    res_index = "normal"

    def update(self, context):
        super().update(context)
        if self.game_object.is_mouse_down:  # 如果被点击，鼠标按下
            self.game_object.is_mouse_up = False
            self.game_object.is_mouse_down = False
            self.game_object.changing_state(ButtonPressedState(), context)  # 则播放按下动画


class ButtonPressedState(StaticUIState):
    res_index = "normal"
    is_pressed = "first"

    def register(self, obj):
        super().register(obj)
        if self.res:
            w, h = self.game_object.surface.get_size()
            temp_surface = pygame.Surface((w, h), pygame.SRCALPHA)
            shrink_surface = pygame.transform.smoothscale(
                self.game_object.surface, (int(w*0.9), int(h*0.9)))
            temp_surface.blit(shrink_surface, (int(w*0.05), int(h*0.05)))
            self.game_object.surface = temp_surface

    def update(self, context):
        super().update(context)
        if self.game_object.is_mouse_up:  # 如果鼠标抬起
            self.game_object.is_mouse_up = False
            self.game_object.is_mouse_down = False
            self.game_object.changing_state(ButtonNormalState(), context)  # 则播放抬起动画
