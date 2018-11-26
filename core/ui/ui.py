from pygame.locals import *

from core.entity.game_object import GameObject


class UI(GameObject):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.focus = False
        self.x = x  # 相对坐标
        self.y = y  # 相对坐标
        self.w = w
        self.h = h
        self.screen_rect = Rect((x, y), (w, h))

        self.event_components = []

    def handle_event(self, event):
        if event.name.startswith("mouse"):  # 如果是鼠标事件
            if self.screen_rect.collidepoint(event.pos[0], event.pos[1]):  # 且鼠标在ui的范围内
                for child in self.children:  # 则处理该事件
                    if not event.handled:
                        child.handle_event(event)
                if not event.handled:
                    for component in self.event_components:
                        component.handle_event(event)
        elif self.focus:  # 如果是焦点
            for child in self.children:  # 则处理该事件
                if not event.handled:
                    child.handle_event(event)
            if not event.handled:
                for component in self.event_components:
                    component.handle_event(event)

    def update(self, data):
        if self.inited:
            if self.parent:
                self.screen_rect = Rect((self.x + self.parent.screen_rect.x,
                                         self.y + self.parent.screen_rect.y), (self.w, self.h))
            # 先更新位置，再更新其他
            self.state.update(data)
            for child in self.children:
                child.update(data)

    def draw(self, screen):
        if self.ready:
            self.state.draw(screen)
            for child in self.children:
                child.draw(screen)

    def add_component(self, component):
        self.event_components.append(component)

    def early_update(self, data):
        pass

    def late_update(self, data):
        pass

    def late_draw(self, screen):
        pass
