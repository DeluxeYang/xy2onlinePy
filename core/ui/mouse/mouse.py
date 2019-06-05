from core.ui.ui import UI
from core.ui.mouse.mouse_state import MouseNormalState, MousePressState, MouseDisabledState
from core.ui.mouse.component import MouseComponent


class Mouse(UI):
    def __init__(self):
        super().__init__(res_info={
            "normal": ["gires.wdf", "0x10EB4A95"],
            "disabled": ["gires.wdf", "0x10EB4A95"],
            "press": ["gires.wdf", "0xDCDC20F7"],
            "give": ["gires.wdf", "0xE02D6D08"],
            "protect": ["gires.wdf", "0xE540C0A2"],
        }, x=0, y=0, w=0, h=0, ui_id="")

        self.press_state = MousePressState()
        self.init_state(self.press_state)

        self.disabled_state = MouseDisabledState()
        self.init_state(self.disabled_state)

        self.normal_state = MouseNormalState()
        self.init_state(self.normal_state)

        self.add_component(MouseComponent())

    def press(self):
        self.state = self.press_state

    def disable(self):
        self.state = self.disabled_state

    def normal(self):
        self.state = self.normal_state

    def destroy(self):
        pass
