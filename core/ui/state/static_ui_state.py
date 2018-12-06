from core.ui.state.ui_state import UIState


class StaticUIState(UIState):
    frame_index = "first"

    def register(self, obj):
        super().register(obj)
        if self.frame_index == "first":
            frame = 0
        elif self.frame_index == "middle":
            frame = self.last_frame // 2
        else:
            frame = self.last_frame
        if self.res:
            self.game_object.surface = self.res.image_group[0][frame]
