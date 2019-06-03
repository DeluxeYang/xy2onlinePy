from core.ui.state.ui_state import UIState


class StaticUIState(UIState):
    frame_index = "first"
    frame = 0

    def register(self, obj):
        super().register(obj)
        if self.frame_index == "first":
            self.frame = 0
        elif self.frame_index == "middle":
            self.frame = self.last_frame // 2
        else:
            self.frame = self.last_frame
        if self.res:
            self.set_surface()

    def set_surface(self):
        self.game_object.surface = self.res.image_group[0][self.frame]
