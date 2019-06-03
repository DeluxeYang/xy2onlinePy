from core.ui.state.animated_ui_state import AnimatedUIState
from core.ui.state.static_ui_state import StaticUIState


class ButtonNormalState(StaticUIState):
    res_index = "normal"
    frame_index = "first"

    def update(self, context):
        super().update(context)
        if self.game_object.is_mouse_down or self.game_object.is_mouse_over:  # 如果被点击，鼠标按下
            self.game_object.is_mouse_up = False
            self.game_object.is_mouse_down = False
            self.game_object.down()  # 则播放按下动画


class ButtonPressedState(StaticUIState):
    res_index = "normal"
    frame_index = "middle"

    def update(self, context):
        super().update(context)
        if self.game_object.is_mouse_up:  # 如果鼠标抬起
            self.game_object.is_mouse_up = False
            self.game_object.is_mouse_down = False
            self.game_object.up()  # 则播放抬起动画
        elif not self.game_object.is_mouse_over:
            self.game_object.normal()


class ButtonDownState(AnimatedUIState):
    res_index = "normal"

    def register(self, obj):
        super().register(obj)
        self.last_frame //= 2  # 仅播放前半段动画，即按下动画

    def update(self, context):
        one_loop = super().update(context)
        if one_loop:
            self.game_object.pressed()  # 转换为按下静态状态


class ButtonUpState(AnimatedUIState):
    res_index = "normal"

    def register(self, obj):
        super().register(obj)
        self.first_frame = self.last_frame // 2  # 仅播放后半段动画，即抬起动画

    def update(self, context):
        one_loop = super().update(context)
        if one_loop:  # 如果已经循环了一遍
            if self.game_object.focus:  # 在按键抬起时，需借用focus标志，判断抬起时鼠标是否还在范围之内，在则出发按键回调
                if self.game_object.callback:
                    self.game_object.callback(self.game_object.param)
            self.game_object.focus = False
            self.game_object.normal()
