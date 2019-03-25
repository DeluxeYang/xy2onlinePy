from core.ui.state.static_ui_state import StaticUIState
from core.ui.text_field.text_field import TextField


class TextButtonState(StaticUIState):
    def register(self, obj):
        self.game_object = obj
        self.game_object.inited = True
        self.game_object.ready = True


class TextButtonNormalState(TextButtonState):
    def register(self, obj):
        super().register(obj)
        self.game_object.is_mouse_down = False
        self.game_object.is_mouse_up = False
        self.game_object.is_mouse_over = False
        self.game_object.empty_children()
        self.game_object.add_child(TextField(
            self.game_object.text, 0, 0, self.game_object.w, self.game_object.h,
            font_name=self.game_object.font_name,
            font_size=self.game_object.font_size,
            sys_font=self.game_object.sys_font,
            color=self.game_object.default_color
        ))

    def update(self, context):
        super().update(context)
        if self.game_object.is_mouse_over:
            self.game_object.changing_state(TextButtonOverState(), context)
        elif self.game_object.is_mouse_down:
            self.game_object.changing_state(TextButtonDownState(), context)


class TextButtonOverState(TextButtonState):
    def register(self, obj):
        super().register(obj)
        self.game_object.empty_children()
        self.game_object.add_child(TextField(
            self.game_object.text, 0, 0, self.game_object.w, self.game_object.h,
            font_name=self.game_object.font_name,
            font_size=self.game_object.font_size,
            sys_font=self.game_object.sys_font,
            color=self.game_object.focus_color, underline=True
        ))

    def update(self, context):
        super().update(context)
        if self.game_object.is_mouse_down:  # 如果鼠标按下
            self.game_object.changing_state(TextButtonDownState(), context)
        elif not self.game_object.is_mouse_over:  # 如果没有按下，且鼠标已经离开
            self.game_object.changing_state(TextButtonNormalState(), context)


class TextButtonDownState(TextButtonState):
    def register(self, obj):
        super().register(obj)
        self.game_object.empty_children()
        self.game_object.add_child(TextField(
            '(*)'+self.game_object.text, 0, 0, self.game_object.w, self.game_object.h,
            font_name=self.game_object.font_name,
            font_size=self.game_object.font_size,
            sys_font=self.game_object.sys_font,
            color=self.game_object.focus_color, underline=True
        ))

    def update(self, context):
        super().update(context)
        if not self.game_object.is_chosen:
            if self.game_object.is_mouse_up and self.game_object.focus:
                if self.game_object.callback:
                    self.game_object.callback(self.game_object.param)
                self.game_object.changing_state(TextButtonNormalState(), context)
