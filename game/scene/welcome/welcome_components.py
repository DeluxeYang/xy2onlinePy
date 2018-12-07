from core.ui.ui_mouse_component import UIMouseComponent


class WelcomeEnterButtonMouseComponent(UIMouseComponent):
    def on_mouse_over(self, event):
        if self.is_mouse_in_rect(event):
            pass

    def on_mouse_left_up(self, event):
        if self.is_mouse_in_rect(event):
            def callback(param):  # Button按键事件回调
                print(param)
            self.game_object.callback = callback
            self.game_object.param = "进入游戏"
            event.handled = True
            self.game_object.focus = True  # 如果鼠标仍在范围之内
        self.game_object.is_mouse_up = True

    def on_mouse_left_down(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.is_mouse_down = True
            event.handled = True


class WelcomeLinkedButtonMouseComponent(UIMouseComponent):
    def on_mouse_over(self, event):
        if self.is_mouse_in_rect(event):
            pass

    def on_mouse_left_up(self, event):
        if self.is_mouse_in_rect(event):
            def callback(param):  # Button按键事件回调
                print(param)
            self.game_object.callback = callback
            self.game_object.param = "打开链接"
            event.handled = True
            self.game_object.focus = True  # 如果鼠标仍在范围之内
        self.game_object.is_mouse_up = True

    def on_mouse_left_down(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.is_mouse_down = True
            event.handled = True


class WelcomeExitButtonMouseComponent(UIMouseComponent):
    def on_mouse_over(self, event):
        if self.is_mouse_in_rect(event):
            pass

    def on_mouse_left_up(self, event):
        if self.is_mouse_in_rect(event):
            def callback(param):  # Button按键事件回调
                print(param)
            self.game_object.callback = callback
            self.game_object.param = "退出游戏"
            event.handled = True
            self.game_object.focus = True  # 如果鼠标仍在范围之内
        self.game_object.is_mouse_up = True

    def on_mouse_left_down(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.is_mouse_down = True
            event.handled = True
