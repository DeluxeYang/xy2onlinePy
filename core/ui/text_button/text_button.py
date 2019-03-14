from core.ui.ui import UI

from core.ui.text_button.text_button_state import TextButtonNormalState
from core.ui.text_button.text_button_base_component import TextButtonBaseComponent


class TextButton(UI):
    def __init__(
            self, text, parent=None, x=0, y=0, w=0, h=0, ui_id="",
            font_name=None, font_size=16, sys_font="simsunnsimsun",
            default_color="#FFFFFF", focus_color="#008800"):
        super().__init__(None, x, y, w, h, ui_id)
        self.text = text
        self.parent = parent

        self.font_name = font_name
        self.font_size = font_size
        self.sys_font = sys_font
        self.default_color = default_color
        self.focus_color = focus_color

        self.is_mouse_down = False
        self.is_mouse_up = False
        self.is_mouse_over = False

        self.init_state(TextButtonNormalState())
        self.add_component(TextButtonBaseComponent())
