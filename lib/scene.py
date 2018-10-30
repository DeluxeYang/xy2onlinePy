from lib.event_component import EventComponent


class Scene:
    def __init__(self, **kwargs):
        self.children = []

        for key, value in kwargs.items():
            self.__setattr__(key, value)

    def handle_event(self, event):
        getattr(self, "_event").update(self, event)

    def update(self, dt):
        pass

    def draw(self, screen):
        pass

    def enter(self, director):
        director.title = self.__dict__.get("title")
        director.resolution = self.__dict__.get("resolution")

    def exit(self, director):
        pass


def scene_factory(init_data):
    init_data["_event"] = EventComponent()
    return Scene(**init_data)
