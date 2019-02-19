from core.ui.ui_mouse_component import UIMouseComponent


class NotifyMouseComponent(UIMouseComponent):
    def on_mouse_left_down(self, event):
        if self.is_mouse_in_rect(event):
            event.handled = True

    def on_mouse_left_up(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.destroy()
            event.handled = True
