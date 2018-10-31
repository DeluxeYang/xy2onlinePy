import pygame

from settings import *
from .scene import scene_factory
from map_client import MapClient
from game_client import NetworkClient

from lib.event.event import Event, events


class Director:
    def __init__(self, title="The Lib", resolution=(800, 600), fps=60):
        pygame.init()
        self.title = title
        self.resolution = resolution
        self.fps = fps

        self.running = True
        self._screen = None
        self._scene = None
        self.old_scene = None
        self.map_client = MapClient("localhost", ResourcePort)
        self.network_client = NetworkClient()

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

    def change_scene(self, scene):
        scene.enter(self)
        self.old_scene = self._scene
        self._scene = scene
        if self.old_scene:
            self.old_scene.exit(self)

    async def run(self, loop, scene=None):
        if scene is None:
            if self._scene is None:
                raise ValueError('No scene provided')
        else:
            self.change_scene(scene)

        if self._screen is None:
            self._scene.set_screen()

        await self.map_client.connect(loop)

        fps = pygame.time.Clock()

        while self.running:
            # event pack
            event_queue = []
            for event in pygame.event.get():
                _dict = event.__dict__
                if event.type in events:
                    thing = events[event.type]
                    if isinstance(thing, dict):  # 如果有二级列表
                        _dict["name"] = thing[_dict["button"]]
                    else:
                        _dict["name"] = thing
                    event_queue.append(Event(**_dict))
            # handle_event
            self.handle_events(event_queue)
            # update
            dt = fps.tick(self.fps)

            self.update(dt)
            # draw
            self.draw(self._screen)

            pygame.display.flip()

    def handle_events(self, event_queue):
        for event in event_queue:  # 循环遍历每个事件
            if hasattr(self, "on_"+event.name):  # 如果self有该事件的处理方法
                getattr(self, "on_"+event.name)(event)  # 则处理
            if not event.handled:  # 如果该事件没有被handle
                self._scene.handle_event(event)  # 则继续向下级传递

    def update(self, dt):
        self._scene.update(dt)

    def draw(self, screen):
        self._scene.draw(screen)

    def get_new_scene(self, map_id):
        return scene_factory(map_id, self)

    def on_change_scene(self, event):
        pass

    def on_change_screen(self,event):
        pass

    def on_quit(self, event):
        self.running = False
        self.map_client.disconnect()
        event.handled = True


director = Director()
