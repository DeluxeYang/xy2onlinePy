from core.ui.state.ui_state import UIState
from utils import ptext


class TextFieldState(UIState):
    def register(self, obj):
        self.game_object = obj
        self.game_object.inited = True
        self.game_object.ready = True

    def draw(self, screen):
        for content in self.game_object.content:
            content.draw(screen)