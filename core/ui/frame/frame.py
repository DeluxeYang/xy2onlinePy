from core.ui.ui import UI
from core.ui.frame.frame_state import FrameState, AnimatedFrameState


class FixedFrame(UI):
    def __init__(self, res_info, x=0, y=0, w=0, h=0, ui_id=""):
        super().__init__(res_info, x, y, w, h, ui_id)
        self.init_state(FrameState())

    def add_child(self, child):
        super().add_child(child)
        if hasattr(child, "ui_id"):
            self.__setattr__(child.ui_id, child)


class AnimatedFrame(UI):
    def __init__(self, res_info, x=0, y=0, w=0, h=0, ui_id=""):
        super().__init__(res_info, x, y, w, h, ui_id)
        self.init_state(AnimatedFrameState())


class MovableFrame(FixedFrame):
    def __init__(self, res_info, x=0, y=0, w=0, h=0):
        super().__init__(res_info, x, y, w, h)
