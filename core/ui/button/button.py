from core.ui.ui import UI
from core.ui.button.button_state import ButtonNormalState,\
    ButtonDownState, ButtonUpState, ButtonPressedState
from utils.res_manager import res_manager
from settings import logger


class Button(UI):
    def __init__(self, res_info, x=0, y=0, w=0, h=0, ui_id=""):
        super().__init__(res_info, x, y, w, h, ui_id)

        self.is_mouse_down = False
        self.is_mouse_up = False
        self.is_mouse_over = False

        self.binding_res()

        self.down_state = ButtonDownState()
        self.init_state(self.down_state)

        self.up_state = ButtonUpState()
        self.init_state(self.up_state)

        self.pressed_state = ButtonPressedState()
        self.init_state(self.pressed_state)

        self.normal_state = ButtonNormalState()
        self.init_state(self.normal_state)

    def binding_res(self):
        address = self.res_info['normal']
        self.res = res_manager.get_res(address[0], address[1])
        logger.debug("res_info：" + str(self.res_info) + "，宽：" + str(self.res.w) + "，高：" + str(self.res.h))

    def normal(self):
        self.state = self.normal_state
        self.state.set_surface()

    def pressed(self):
        self.state = self.pressed_state
        self.state.set_surface()

    def down(self):
        self.state = self.down_state

    def up(self):
        self.state = self.up_state

