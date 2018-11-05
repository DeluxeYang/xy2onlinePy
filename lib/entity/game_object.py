from pygame.locals import *

from lib.state.state import State
from lib.component.component import Component


class GameObject:
    """
    组件与状态混用
    """
    def __init__(self):
        self.rect = Rect((0, 0), (0, 0))  # GameObject矩形

        self.x = 0  # GameObject关键点 X
        self.y = 0  # GameObject关键点 Y
        self.z = 0  # GameObject Z序

        self._state = None

        self.inited = False
        self.ready = False

        self.components = []
        self.event_components = []
        self.early_update_components = []
        self.update_components = []
        self.late_update_components = []
        self.draw_components = []

    def add_components(self, *components):
        for component in components:
            self.add_component(component)

    def add_component(self, component):
        if isinstance(component, Component):
            component.register(self)

    def init_state(self, state):
        if isinstance(state, State):  # 如果是State实例
            self._state = state
            self._state.register(self)

    def send_message(self, message, data=None):
        for component in self.components:
            result = component.handle_message(message, data)
            if result is not None:
                return result

    def handle_event(self, event):
        for component in self.event_components:
            component.handle_event(event)

    def update(self, data):
        if self.inited:
            for component in self.early_update_components:
                component.early_update()
            for component in self.update_components:
                component.update(data)
            self._state.update(data)
            for component in self.late_update_components:
                component.late_update()

    def draw(self, screen):
        if self.ready:
            for component in self.draw_components:
                component.draw(screen)
            self._state.draw(screen)
            self._state.late_draw(screen)
