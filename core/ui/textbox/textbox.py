from core.entity.ui import UI


class TextBox(UI):
    def __init__(self, parent, target, x, y, w, h):
        super().__init__(x, y, w, h)
        self.target = target
        self.text = str(target)

        self.parent = parent
        self.parent.add_child(self)


