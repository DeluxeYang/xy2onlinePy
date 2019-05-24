from core.ui.button.button_component import ButtonComponent
from core.event.event import post_event

from game.scene.notice.notice_scene import NoticeScene


class WelcomeEnterButtonMouseComponent(ButtonComponent):
    def on_mouse_left_up(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.callback = post_event
            self.game_object.param = {"name": "change_scene",
                                      "scene": NoticeScene}
            event.handled = True
            self.game_object.focus = True  # 如果鼠标仍在范围之内
        self.game_object.is_mouse_up = True

    def on_mouse_left_down(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.is_mouse_down = True
            event.handled = True


class WelcomeLinkedButtonMouseComponent(ButtonComponent):
    def on_mouse_over(self, event):
        if self.is_mouse_in_rect(event):
            pass

    def on_mouse_left_up(self, event):
        if self.is_mouse_in_rect(event):
            import webbrowser
            webbrowser.open("http://xy2.163.com")
            event.handled = True
            self.game_object.focus = True  # 如果鼠标仍在范围之内
        self.game_object.is_mouse_up = True

    def on_mouse_left_down(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.is_mouse_down = True
            event.handled = True


class WelcomeExitButtonMouseComponent(ButtonComponent):
    def on_mouse_over(self, event):
        if self.is_mouse_in_rect(event):
            pass

    def on_mouse_left_up(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.callback = post_event
            self.game_object.param = {"name": "quit"}
            event.handled = True
            self.game_object.focus = True  # 如果鼠标仍在范围之内
        self.game_object.is_mouse_up = True

    def on_mouse_left_down(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.is_mouse_down = True
            event.handled = True
