import pygame

from core.state.state import State


class GameObject:
    """
    组件与状态混用
    """
    def __init__(self):
        self.surface = pygame.Surface((0, 0))

        self.parent = None
        self.children = []

        self.x = 0  # GameObject关键点 X
        self.y = 0  # GameObject关键点 Y
        self.z = 0  # GameObject Z序

        self.state = None

        self.inited = False
        self.ready = False

    def handle_event(self, event):
        self.state.handle_event(event)

    def early_update(self, data):
        if self.inited:
            self.state.early_update(data)

    def update(self, data):
        if self.inited:
            self.state.update(data)

    def late_update(self, data):
        if self.inited:
            self.state.late_update(data)

    def draw(self, screen):
        if self.ready:
            self.state.draw(screen)

    def late_draw(self, screen):
        if self.ready:
            self.state.late_draw(screen)

    def get_xy(self):
        return self.x, self.y

    def init_state(self, state):
        if isinstance(state, State):  # 如果是State实例
            self.state = state
            self.state.register(self)
            self.state.enter()

    def changing_state(self, next_state, data=None):
        if not isinstance(self.state, type(next_state)):
            self.state.exit()
            self.init_state(next_state)
            if data:
                self.state.update(data)
