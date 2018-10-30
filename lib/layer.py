class Layer:
    def __init__(self, _event, z):
        self.z = z
        self._event = _event
        self.children = []

    def handle_event(self, event):
        self._event.update(self, event)

    def update(self, dt):
        pass

    def draw(self, screen):
        pass


class MapLayer(Layer):
    def __init__(self, surface, z):
        super().__init__(z)
        self.surface = surface