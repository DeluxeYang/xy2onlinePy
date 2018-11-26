from core.ui.state.ui_state import UIState


class StaticUIState(UIState):
    def register(self, obj):
        super().register(obj)
        self.game_object.surface = self.res.image_group[0][0]
