from core.ui.ui import UI
from core.ui.textfield.textfield import TextField


class TextInput(UI):
    def __init__(self, x, y, w, h):
        super().__init__(None, x, y, w, h)
        self.text = ""
        self.text_field = TextField(self.text, x, y, w, h, font_name=None, sys_font="simsunnsimsun")

    def remove_children(self):
        for child in self.children:
            child.destroy()
        self.children = []

    def update_text_field(self):
        self.text_field = TextField(self.text, self.x, self.y, self.w, self.h,
                                    font_name=None, sys_font="simsunnsimsun")
        self.add_child(self.text_field)
