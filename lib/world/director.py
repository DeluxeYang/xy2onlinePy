import pygame
from pygame.locals import *

from .scene import scene_factory

from lib.event.event import Event, events

from map_client import map_client, map_connection

class Director:

    def __init__(self, network_client, title="The Lib", resolution=(800, 600), fps=60):
        pygame.init()
        self.title = title
        self.resolution = resolution
        self.fps = fps

        self.running = True
        self.run_task = None
        self._screen = None
        self._scene = None
        self.old_scene = None

        self.map_connection = map_connection
        self.map_client = map_client
        self.network_client = network_client

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

    def run(self, scene=None):
        if scene is None:
            if self._scene is None:
                raise ValueError('No scene provided')
        else:
            self.change_scene(scene)

        if self._screen is None:
            self._scene.set_screen()

        fps = pygame.time.Clock()

        running_data = {
            "delta_time": 0.0,
            "current_time": 0.0,
            "other_masks": [],
            "left_top": (0, 0),
            "collision_window": Rect((0, 0), (0, 0)),
            "me_world_pc": (0, 0),
        }

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
                    event_queue.append(Event(_dict))
                elif event.type == USEREVENT:
                    event_queue.append(Event(_dict))
            # handle_event
            self.handle_events(event_queue)
            # update
            running_data["delta_time"] = fps.tick(self.fps)
            running_data["current_time"] = pygame.time.get_ticks()

            self.update(running_data)

            self._screen.fill((0, 0, 0))

            self.draw(self._screen)

            pygame.display.flip()

            self.map_connection.pump()
            self.map_client.pump()

    def handle_events(self, event_queue):
        for event in event_queue:  # 循环遍历每个事件
            if hasattr(self, "on_"+event.name):  # 如果self有该事件的处理方法
                getattr(self, "on_"+event.name)(event)  # 则处理
            if not event.handled:  # 如果该事件没有被handle
                self._scene.handle_event(event)  # 则继续向下级传递

    def update(self, data):
        self._scene.update(data)

    def draw(self, screen):
        self._scene.draw(screen)

    def get_new_scene(self, map_id):
        return scene_factory(map_id, self)

    def on_change_scene(self, event):
        pass

    def on_change_screen(self, event):
        pass

    def on_quit(self, event):
        self.running = False
        event.handled = True
