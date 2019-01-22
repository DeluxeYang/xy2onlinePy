from core.ui.ui import UI
from core.ui.button.button_state import ButtonNormalState


class Button(UI):
    def __init__(self, res_info, x=0, y=0, w=0, h=0):
        super().__init__(res_info, x, y, w, h)

        self.is_mouse_down = False
        self.is_mouse_up = False

        self.init_state(ButtonNormalState())
