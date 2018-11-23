from core.entity.ui import UI
from utils import ptext


class TextBox(UI):
    def __init__(self, parent, target, x=0, y=0, w=0, h=0):
        super().__init__(x, y, w, h)
        self.target = target
        self.text = str(target)

        self.parent = parent
        self.parent.add_child(self)


