from core.ui.ui import UI
from core.ui.text_field.text_field import TextField
from core.ui.fps.state import FPSState


class FPS(UI):
    def __init__(self):
        super().__init__(None, 0, 100, 100, 20, "")
        self.text = ""

        self.text_field = TextField(self.text, 0, 0, self.w, self.h, color="#00FF00")

        self.add_child(self.text_field)

        self.init_state(FPSState())
