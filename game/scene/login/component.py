from core.ui.button.button_component import ButtonComponent
from core.event.event import post_event
from core.world.director import network_client


class EnterButtonMouseComponent(ButtonComponent):
    def on_mouse_left_up(self, event):
        if self.is_mouse_in_rect(event):
            network_client.request(send_data={
                "action": "login",
                "account": self.game_object.parent.username_input.input_string
            })
            event.handled = True
            self.game_object.focus = True  # 如果鼠标仍在范围之内
        self.game_object.is_mouse_up = True

    def on_mouse_left_down(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.is_mouse_down = True
            event.handled = True


class CancelButtonMouseComponent(ButtonComponent):
    def on_mouse_left_up(self, event):
        if self.is_mouse_in_rect(event):
            from game.scene.welcome.welcome_scene import WelcomeScene
            self.game_object.callback = post_event
            self.game_object.param = {"name": "change_scene",
                                      "scene": WelcomeScene}
            event.handled = True
            self.game_object.focus = True  # 如果鼠标仍在范围之内
        self.game_object.is_mouse_up = True

    def on_mouse_left_down(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.is_mouse_down = True
            event.handled = True
