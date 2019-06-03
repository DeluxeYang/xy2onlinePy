from core.ui.ui_mouse_component import UIMouseComponent


class ButtonComponent(UIMouseComponent):
    def on_mouse_over(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.is_mouse_over = True
        else:
            self.game_object.is_mouse_over = False
