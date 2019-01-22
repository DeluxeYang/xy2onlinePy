from core.ui.ui import UI
from core.ui.frame.frame_state import FrameState
from core.ui.text_input.text_input import TextInput


class FixedFrame(UI):
    def __init__(self, res_info, x=0, y=0, w=0, h=0):
        super().__init__(res_info, x, y, w, h)
        self.init_state(FrameState())

    def add_child(self, child):
        super().add_child(child)
        if isinstance(child, TextInput):
            self.__setattr__(child.input_id, child)


class MovableFrame(FixedFrame):
    def __init__(self, res_info, x=0, y=0, w=0, h=0):
        super().__init__(res_info, x, y, w, h)
