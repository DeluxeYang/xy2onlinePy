from core.ui.ui_mouse_component import UIMouseComponent
from core.event.event import post_event
from res.characters import characters


class CharacterButtonComponent(UIMouseComponent):
    def __init__(self, race, version, name):
        super().__init__()
        self.race = race
        self.version = version
        self.name = name
        self.res_info = characters[race][version][name]

    def on_mouse_left_up(self, event):
        if self.is_mouse_in_rect(event):
            event.handled = True
            self.game_object.focus = True  # 如果鼠标仍在范围之内
        self.game_object.is_mouse_up = True

    def on_mouse_left_down(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.is_mouse_down = True
            event.handled = True