from core.entity.ui import UI
from utils import ptext


class Button(UI):
    def __init__(self, parent, text=None, x=0, y=0, w=0, h=0):
        super().__init__(x, y, w, h)
        self.text = str(text)

        self.parent = parent
        self.parent.add_child(self)
