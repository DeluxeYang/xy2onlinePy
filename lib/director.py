import pygame
from pygame.locals import *

from .event import Event, events


class Director:
    def __init__(self, title="The Lib", resolution=(800, 600), fps=60):
        pygame.init()
        self.title = title
        self.resolution = resolution
        self.fps = fps
        self._screen = None
        self._scene = None
        self.old_scene = None

    @property
    def title(self):
        return pygame.display.get_caption()

    @title.setter
    def title(self, value):
        pygame.display.set_caption(value)

    @property
    def resolution(self):
        return self._screen.get_size()

    @resolution.setter
    def resolution(self, value):
        self._screen = pygame.display.set_mode(value)

    @property
    def _scene(self):
        return self._scene

    @_scene.setter
    def _scene(self, scene):
        self._scene = scene

    def change_scene(self, scene):
        pass

    def run(self, scene=None):
        if scene is None:
            if self._scene is None:
                raise ValueError('No scene provided')
        else:
            self.change_scene(scene)

        if self._screen is None:
            self._scene.set_screen()

        fps = pygame.time.Clock()

        while self._scene is not None:
            # event pack
            event_queue = []
            for event in pygame.event.get():
                _dict = event.__dict__
                _dict["name"] = events.get(event.type, _dict["name"])
                event_queue.append(Event(**_dict))
            # handle_event
            self._scene.handle_event()
            # update
            dt = fps.tick(self.fps)

            self.update(dt)
            # draw
            self.draw(self._screen)

            pygame.display.flip()

    def handle_event(self, event_queue):
        for event in event_queue:  # 循环遍历每个事件
            if hasattr(self, "on_"+event.name):  # 如果self有该事件的处理方法
                getattr(self, "on_"+event.name)(event)  # 则处理
            if not event.handled:  # 如果该事件没有被handle
                self._scene.handle_event(event)  # 则继续向下级传递

    def update(self, dt):
        self._scene.update(dt)

    def draw(self, screen):
        self._scene.draw(screen)

    def on_change_scene(self, event):
        pass

    def on_change_screen(self,event):
        pass

    def on_quit(self, event):
        pass