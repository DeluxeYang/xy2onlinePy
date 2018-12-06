from core.ui.ui import UI
from core.ui.frame.frame_state import FrameState


class FixedFrame(UI):
    def __init__(self, res_info, x=0, y=0, w=0, h=0):
        super().__init__(res_info, x, y, w, h)
        self.init_state(FrameState())


class MovableFrame(FixedFrame):
    def __init__(self, res_info, x=0, y=0, w=0, h=0):
        super().__init__(res_info, x, y, w, h)
