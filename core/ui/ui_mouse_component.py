from core.ui.ui_component import UIComponent
from core.event.event import post_event


class UIMouseComponent(UIComponent):
    def is_mouse_in_rect(self, event, reset_focus=True):
        flag = self.game_object.screen_rect.collidepoint(event.pos[0], event.pos[1])  # 且鼠标在ui的范围内
        if flag and reset_focus:
            post_event({"name": "reset_ui_focus", "set_focus_obj": self.game_object})
        return flag
