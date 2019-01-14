from core.ui.ui_mouse_component import UIMouseComponent
from core.event.event import post_event

from game.scene.world.world_scene import WorldScene


class NoticeEnterButtonMouseComponent(UIMouseComponent):
    def on_mouse_over(self, event):
        if self.is_mouse_in_rect(event):
            pass

    def on_mouse_left_up(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.callback = post_event
            self.game_object.param = {"name": "change_scene",
                                      "scene": WorldScene}
            event.handled = True
            self.game_object.focus = True  # 如果鼠标仍在范围之内
        self.game_object.is_mouse_up = True

    def on_mouse_left_down(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.is_mouse_down = True
            event.handled = True
