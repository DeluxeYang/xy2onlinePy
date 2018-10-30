class Scene:
    def __init__(self, _event, title="The Lib", resolution=(800, 600), fps=60):
        self.title = title
        self.resolution = resolution
        self.fps = fps
        self.children = []
        self._event = _event

    def handle_event(self, event):
        self._event.update(self, event)

    def update(self, dt):
        pass

    def draw(self, screen):
        pass

    def set_screen(self, director):
        director.resolution = self.resolution

    def on_enter(self, event):
        pass

    def on_exit(self, event):
        pass
