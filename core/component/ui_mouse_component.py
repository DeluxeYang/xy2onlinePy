from core.component.component import Component


class UIMouseComponent(Component):
    def is_mouse_in_rect(self, event):
        return self.state.game_object.screen_rect.collidepoint(event.pos[0], event.pos[1])  # 且鼠标在ui的范围内