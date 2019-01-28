from core.ui.ui import UI
from core.ui.text_field.text_field import TextField
from core.ui.notify.notify_state import NotifyState


class Notify(UI):
    def __init__(self, res_info, text, x, y, w, h,
                 font_name=None, font_size=16, sys_font="simsunnsimsun",
                 default_color="#00FF00", focus_color="#008800"):
        super().__init__(res_info, x, y, w, h)
        self.text = text

        self.font_name = font_name
        self.font_size = font_size
        self.sys_font = sys_font
        self.default_color = default_color
        self.focus_color = focus_color

        self.add_child(TextField(
            self.text, 0, 0, self.w, self.h,
            font_name=self.font_name, font_size=self.font_size,
            sys_font=self.sys_font, color=self.default_color))

        self.init_state(NotifyState())

