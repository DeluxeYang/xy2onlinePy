from core.ui.ui_mouse_component import UIMouseComponent
from core.event.event import post_event
from core.world.director import network_client
from res.characters import characters
from core.ui.frame.frame_state import AnimatedFrameState
from core.ui.text_field.text_field_state import TextFieldState


class CharacterButtonComponent(UIMouseComponent):
    """
    角色头像按键
    """
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
                frames[i].changing_state(AnimatedFrameState(res_info, "hit"), force=True)
                i += 1
            self.game_object.parent.store["character_race"] = self.race
            self.game_object.parent.store["character_version"] = self.version
            self.game_object.parent.store["character_name"] = self.name
            self.game_object.parent.character_introduction.update_text(self.res_info["describe"])
        self.game_object.is_mouse_up = True

    def on_mouse_left_down(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.is_mouse_down = True
            event.handled = True


class LeaveButtonComponent(UIMouseComponent):
    """
    离开
    """
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


class CreateButtonComponent(UIMouseComponent):
    """
    创建
    """
    def on_mouse_left_up(self, event):
        if self.is_mouse_in_rect(event):
            event.handled = True
            self.game_object.focus = True  # 如果鼠标仍在范围之内
            role_name = self.game_object.parent.role_name_input.input_string
            if role_name == "":  # 如果角色名为空
                post_event({"name": "notify", "text": "请输入角色名"})
            else:
                network_client.request(send_data={
                    "action": "create_role",
                    "role_name": role_name,
                    "character_race": self.game_object.parent.store["character_race"],
                    "character_version": self.game_object.parent.store["character_version"],
                    "character_name": self.game_object.parent.store["character_name"]
                })
        self.game_object.is_mouse_up = True

    def on_mouse_left_down(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.is_mouse_down = True
            event.handled = True
