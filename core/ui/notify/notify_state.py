from core.ui.state.static_ui_state import StaticUIState
import pygame


class NotifyState(StaticUIState):
    res_index = "normal"

    def __init__(self):
        super().__init__()
        self.clock = pygame.time.Clock()
        self.ms_counter = 0

    def update(self, context):
        super().update(context)
        self.ms_counter += self.clock.get_time()
        self.clock.tick()
        if self.ms_counter > 5000:
            self.game_object.destroy()



