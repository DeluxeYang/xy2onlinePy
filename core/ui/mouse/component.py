from core.ui.ui_component import UIComponent


class MouseComponent(UIComponent):
    def on_mouse_over(self, event):
        self.game_object.x = event.pos[0]
        self.game_object.y = event.pos[1]
