from core.ui.state.animated_ui_state import AnimatedUIState
from core.ui.state.static_ui_state import StaticUIState


class ButtonNormalState(StaticUIState):
    res_index = "normal"
    frame_index = "first"

    def update(self, data):
        super().update(data)
        if self.game_object.is_mouse_down:
            self.game_object.is_mouse_down = False
            self.game_object.changing_state(ButtonMouseUpState(), data)  # 则转换为静态状态


class ButtonPressedState(StaticUIState):
    res_index = "normal"
    frame_index = "middle"

    def update(self, data):
        super().update(data)
        if self.game_object.is_mouse_up:
            self.game_object.is_mouse_up = False
            self.game_object.changing_state(ButtonMouseUpState(), data)  # 则转换为静态状态


class ButtonMouseDownState(AnimatedUIState):
    res_index = "normal"
    is_mouse_already_up = False

    def register(self, obj):
        super().register(obj)
        self.last_frame //= 2

    def update(self, data):
        one_loop = super().update(data)
        if self.game_object.is_mouse_up:
            self.is_mouse_already_up = True
            self.game_object.is_mouse_up = False
        if one_loop:
            if not self.is_mouse_already_up:
                self.game_object.changing_state(ButtonPressedState(), data)  # 则转换为静态状态
            else:
                self.game_object.changing_state(ButtonMouseUpState(), data)  # 则转换为静态状态


class ButtonMouseUpState(AnimatedUIState):
    res_index = "normal"

    def register(self, obj):
        super().register(obj)
        # self.first_frame = self.last_frame // 2 + 1

    def update(self, data):
        one_loop = super().update(data)
        if one_loop:  # 如果已经循环了一遍
            self.game_object.callback(self.game_object.param)
            self.game_object.changing_state(ButtonNormalState(), data)
