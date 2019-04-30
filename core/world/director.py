import gc

import pygame
from pygame.locals import *

from core.event.event import event_filter

# from map_client import map_client, map_connection
from network_client import network_client, network_connection


class Director:
    def __init__(self, title="Director", resolution=(640, 480), fps=60):
        pygame.init()
        self.title = title
        self.resolution = resolution
        self.fps = fps
        self.clock = pygame.time.Clock()

        self.running = True
        self._screen = None
        self._scene = None
        self.old_scene = None

        self.account = None

        # self.map_connection = map_connection
        # self.map_client = map_client

        self.network_connection = network_connection
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

    def run(self, scene=None):
        if scene is None:
            if self._scene is None:
                raise ValueError('No scene provided')
        else:
            self.change_scene(scene)

        context = {
            "delta_time": 0.0,
            "current_time": 0.0,
            "portals": [],
            "other_masks": [],
            "left_top": (0, 0),
            "collision_window": Rect((0, 0), (0, 0)),
            "me_world_pc": (0, 0),
        }
        while self.running:
            event_queue = event_filter()
            # handle_event
            self.handle_events(event_queue)
            # running_data setting
            context["delta_time"] = self.clock.tick(self.fps)
            context["current_time"] = pygame.time.get_ticks()

            self.update(context)

            self._screen.fill((0, 0, 0))

            self.draw(self._screen)

            pygame.display.flip()
            # map_client pump
            # self.map_connection.pump()
            # self.map_client.pump()
            # network_client pump
            self.network_connection.pump()
            self.network_client.pump()

            gc.collect()

    def handle_events(self, event_queue):
        for event in event_queue:  # 循环遍历每个事件
            if hasattr(self, "on_"+event.name):  # 如果self有该事件的处理方法
                getattr(self, "on_"+event.name)(event)  # 则处理
            if not event.handled:  # 如果该事件没有被handle
                self._scene.handle_event(event)  # 则继续向下级传递

    def update(self, context):
        self._scene.update(context)

    def draw(self, screen):
        self._scene.draw(screen)

    def get_new_scene(self, character_id, map_id):
        pass

    def change_scene(self, the_scene_class):
        scene = the_scene_class()
        scene.enter()
        if self._scene:
            self._scene.exit()
            self._scene = None
        self._scene = scene

    def on_change_scene(self, event):
        self.change_scene(event.scene)

    def on_changing_screen(self, event):
        pass

    def on_quit(self, event):
        self.running = False
        event.handled = True


director = Director()
