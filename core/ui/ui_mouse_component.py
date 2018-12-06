from core.ui.ui_component import UIComponent


class UIMouseComponent(UIComponent):
    def is_mouse_in_rect(self, event):
        return self.game_object.screen_rect.collidepoint(event.pos[0], event.pos[1])  # 且鼠标在ui的范围内