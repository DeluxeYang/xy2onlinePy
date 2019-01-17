from core.ui.ui_mouse_component import UIMouseComponent


class TextButtonBaseComponent(UIMouseComponent):
    def on_mouse_over(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.is_mouse_over = True
        else:
            self.game_object.is_mouse_over = False

    def on_mouse_left_down(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.is_mouse_down = True
            event.handled = True

    def on_mouse_left_up(self, event, callback=None, param=None):
        if self.is_mouse_in_rect(event):
            self.game_object.callback = callback
            self.game_object.param = param
            event.handled = True
            self.game_object.focus = True
        self.game_object.is_mouse_up = True
