from core.entity.ui import UI


class Label(UI):
    def __init__(self, parent, x, y, text=""):
        super().__init__()
        self.text = text

        self.x = x
        self.y = y
        self.parent = parent
        self.parent.add_child(self)
