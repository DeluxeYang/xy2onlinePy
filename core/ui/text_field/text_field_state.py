from core.ui.state.ui_state import UIState
from utils import ptext


class TextFieldState(UIState):
    def __init__(self, text=None):
        super().__init__()
        self.text = text

    def register(self, obj):
        self.game_object = obj
        self.game_object.inited = True  # 初始化完成
        self.game_object.ready = True
        if self.text:
            self.game_object.empty_children()
            contents = self.game_object.translate_and_split(self.text)
            self.game_object.rebuild(contents)
