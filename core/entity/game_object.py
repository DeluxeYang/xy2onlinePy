import pygame
import random
import string

from core.state.state import State
from core.ui.state.ui_state import UIState


class GameObject:
    """
    组件与状态混用
    """
    def __init__(self, x, y, z=0):
        self.surface = pygame.Surface((0, 0))
        self.id = ''.join(random.sample(string.ascii_letters, 10))

        self.parent = None
        self.children = []

        self.res_info = None

        self.x = x  # GameObject关键点 X
        self.y = y  # GameObject关键点 Y
        self.z = z  # GameObject Z序
        self.z_index = 0

        self.state = None

        self.inited = False
        self.ready = False

    def handle_event(self, event):
        self.state.handle_event(event)

    def early_update(self, context):
        if self.inited:
            self.state.early_update(context)

    def update(self, context):
        if self.inited:
            self.state.update(context)

    def late_update(self, context):
        if self.inited:
            self.state.late_update(context)

    def draw(self, screen):
        if self.ready:
            self.state.draw(screen)

    def late_draw(self, screen):
        if self.ready:
            self.state.late_draw(screen)

    def get_xy(self):
        return self.x, self.y

    def init_state(self, state):
        if isinstance(state, State) or isinstance(state, UIState):  # 如果是State实例
            self.state = state
            self.state.register(self)
            self.state.enter()

    def changing_state(self, next_state, context=None, force=False):
        if not force and isinstance(next_state, type(self.state)):
            return
        self.state.exit()
        self.init_state(next_state)
        if context:
            self.state.update(context)

    def add_child(self, child):
        child.parent = self
        while hasattr(self, child.id):  # 如果child id已经在self这里重复，则重新随机child id
            child.id = ''.join(random.sample(string.ascii_letters, 10))
        self.__setattr__(child.id, child)
        child.z = self.z_index
        self.z_index += 1
        self.children.append(child)

    def destroy(self):
        for child in self.children:
            child.destroy()
            del child
        self.children = []

        self.state.destroy()
        self.state = None

        if self.parent:
            i = 0
            for me_or_brothers in self.parent.children:
                if me_or_brothers.id == self.id:
                    break
                i += 1
            del self.parent.children[i]
            self.parent.__delattr__(self.id)
        self.parent = None

        self.surface = None
        del self

    def empty_children(self):
        self.children.clear()
