from core.ui.state.animated_ui_state import AnimatedUIState
from core.ui.state.static_ui_state import StaticUIState


class ButtonStaticState(StaticUIState):
    def update(self, data):
        super().update(data)
        if self.game_object.is_pressed:
            self.game_object.is_pressed = False
            self.game_object.changing_state(ButtonPressedState(), data)  # 则转换为静态状态


class ButtonPressedState(AnimatedUIState):
    def update(self, data):
        one_loop = super().update(data)
        if one_loop:  # 如果已经循环了一遍
            self.game_object.changing_state(ButtonStaticState(), data)  # 则转换为静态状态
