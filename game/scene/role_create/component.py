from core.ui.ui_mouse_component import UIMouseComponent
from core.event.event import post_event
from res.characters import characters
from core.ui.frame.frame_state import AnimatedFrameState
from core.ui.text_field.text_field_state import TextFieldState


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
            frames = [self.game_object.parent.first_weapon, self.game_object.parent.second_weapon]
            i = 0
            for weapon, res_info in self.res_info["weapon"].items():
                frames[i].changing_state(AnimatedFrameState(res_info, "hit"))
                i += 1
            self.game_object.parent.character_introduction.\
                changing_state(TextFieldState(self.res_info["describe"]))
        self.game_object.is_mouse_up = True

    def on_mouse_left_down(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.is_mouse_down = True
            event.handled = True


class LeaveButtonComponent(UIMouseComponent):
    def on_mouse_left_up(self, event):
        if self.is_mouse_in_rect(event):
            from game.scene.role_select.role_select_scene import RoleSelectScene
            self.game_object.callback = post_event
            self.game_object.param = {"name": "change_scene",
                                      "scene": RoleSelectScene}
            event.handled = True
            self.game_object.focus = True  # 如果鼠标仍在范围之内
        self.game_object.is_mouse_up = True

    def on_mouse_left_down(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.is_mouse_down = True
            event.handled = True
