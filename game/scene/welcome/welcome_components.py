from core.ui.ui_mouse_component import UIMouseComponent


class EnterButtonMouseComponent(UIMouseComponent):
    def on_mouse_over(self, event):
        if self.is_mouse_in_rect(event):
            pass

    def on_mouse_left_up(self, event):
        def callback(param):
            print(param)
        self.game_object.callback = callback
        self.game_object.param = "ASD"
        self.game_object.is_mouse_up = True

    def on_mouse_left_down(self, event):
        self.game_object.is_mouse_down = True
