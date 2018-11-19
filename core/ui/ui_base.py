from pygame.locals import *

from core.entity.game_object import GameObject


class UI(GameObject):
    def __init__(self):
        super().__init__()
        self.focus = False
        self.screen_rect = Rect((0, 0), (0, 0))

    def handle_event(self, event):
        if self.focus or event.name[:5] == "mouse":  # 如果是焦点，或者，是鼠标事件
            for child in self.children:  # 则处理该事件
                if not event.handled:
                    child.handle_event(event)
            if not event.handled:
                self.state.handle_event(event)

    def update(self, data):
        if self.inited:
            if self.parent:
                self.screen_rect = self.parent.screen_rect.move(self.x, self.y)
            else:
                self.screen_rect = Rect((self.x, self.y), (0, 0))
            # 先更新位置，再更新其他
            self.state.update(data)
            for child in self.children:
                child.update(data)

    def draw(self, screen):
        if self.ready:
            self.state.draw(screen)
            for child in self.children:
                child.draw(screen)

    def early_update(self, data):
        pass

    def late_update(self, data):
        pass

    def late_draw(self, screen):
        pass
