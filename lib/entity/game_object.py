from pygame.locals import *

from lib.component.component import Component


class GameObject:
    def __init__(self, *components):
        self.rect = Rect((0, 0), (0, 0))  # GameObject矩形

        self.x = 0  # GameObject关键点 X
        self.y = 0  # GameObject关键点 Y
        self.z = 0  # GameObject Z序

        self._state = None

        self._components = []

    def add_components(self, *components):
        for component in components:
            self.add_component(component)

    def add_component(self, component):
        if isinstance(component, Component):
            self._components.append(component)
            component.start(self)

    def remove_component(self, component):
        if component is None or not isinstance(component, Component):
            return
        self._components.remove(component)

    def send_message(self, string, data=None):
        for component in self._components:
            result = component.handle_message(string, data)
            if result is not None:
                return result

    def handle_event(self, event):
        for component in self._components:
            component.handle_event(event)

    def update(self, dt):
        for component in self._components:
            component.early_update()
        for component in self._components:
            component.update(dt)
        self._state.update()
        for component in self._components:
            component.late_update()

    def draw(self, screen):
        for component in self._components:
            component.draw(screen)
        self._state.draw(screen)

    def late_draw(self, screen):
        self._state.late_draw(screen)
