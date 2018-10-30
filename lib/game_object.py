class GameObject:
    def __init__(self, _event):
        self._event = _event

    def handle_event(self, event):
        self._event.update(event)

    def update(self):
        pass

    def draw(self):
        pass
