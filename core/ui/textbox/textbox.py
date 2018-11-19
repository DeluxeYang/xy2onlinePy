from core.ui.ui_base import UI


class TextBox(UI):
    def __init__(self, parent, text=""):
        super().__init__()
        self.text = text
        self.parent = parent
        self.parent.add_child(self)
