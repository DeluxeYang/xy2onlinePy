from .state import State


class MapState(State):
    def draw(self, screen):
        if self.game_object.ready:
            screen.blit(self.game_object.surface, (0, 0), self.game_object.window)
