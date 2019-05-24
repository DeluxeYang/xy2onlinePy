from core.ui.ui_mouse_component import UIMouseComponent


class ButtonComponent(UIMouseComponent):
    def on_mouse_over(self, event):
        self.is_mouse_in_rect(event)
