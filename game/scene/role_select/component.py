from core.ui.ui_mouse_component import UIMouseComponent
from core.ui.text_button.text_button_base_component import TextButtonBaseComponent
from core.event.event import post_event
from core.ui.frame.frame_state import AnimatedFrameState
from core.world.director import director


class CreateButtonComponent(UIMouseComponent):
    def on_mouse_left_up(self, event):
        if self.is_mouse_in_rect(event):
            from game.scene.role_create.role_create_scene import RoleCreateScene
            self.game_object.callback = post_event
            self.game_object.param = {"name": "change_scene",
                                      "scene": RoleCreateScene}
            event.handled = True
            self.game_object.focus = True  # 如果鼠标仍在范围之内
        self.game_object.is_mouse_up = True

    def on_mouse_left_down(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.is_mouse_down = True
            event.handled = True


class EnterButtonComponent(UIMouseComponent):
    def on_mouse_left_up(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.focus = True  # 如果鼠标仍在范围之内
        self.game_object.is_mouse_up = True

    def on_mouse_left_down(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.is_mouse_down = True
            event.handled = True


class ExitButtonComponent(UIMouseComponent):
    def on_mouse_left_up(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.focus = True  # 如果鼠标仍在范围之内
        self.game_object.is_mouse_up = True

    def on_mouse_left_down(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.is_mouse_down = True
            event.handled = True


class RoleNameComponent(TextButtonBaseComponent):
    def on_mouse_left_up(self, event, callback=None, param=None):
        if self.is_mouse_in_rect(event):
            self.game_object.focus = True  # 如果鼠标仍在范围之内
            data = self.game_object.parent.store[self.game_object.text]
            self.game_object.parent.level.update_text(str(data["role_level"]))
            self.game_object.parent.gender.update_text(str(data["role_gender"]))
            self.game_object.parent.race.update_text(str(data["role_race"]))
            self.game_object.parent.avatar.changing_state(AnimatedFrameState({'normal': data["role_avatar"]}))
        self.game_object.is_mouse_up = True

    def on_mouse_left_down(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.is_mouse_down = True
            self.set_chosen()
            event.handled = True
