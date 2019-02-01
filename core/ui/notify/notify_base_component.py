from core.ui.ui_mouse_component import UIMouseComponent


class NotifyMouseComponent(UIMouseComponent):
    def on_mouse_left_down(self, event):
        if self.is_mouse_in_rect(event):
            print(self.game_object.z)
            self.game_object.destroy()
            event.handled = True
