import gc, psutil, os
import random

import pygame
from pygame.locals import *

from core.event.event import event_filter
from utils import transitions

from settings import logger, WindowSize
from network_client import network_client, network_connection

process = psutil.Process(os.getpid())


class Director:
    def __init__(self, title="Director", resolution=(640, 480), fps=60):
        pygame.init()
        self.title = title
        self.w, self.h = resolution

        self.fps = fps
        self.clock = pygame.time.Clock()

        self.running = True
        self._screen = pygame.display.set_mode(resolution)
        self._scene = None
        self.old_scene = None

        self.account = None

        self.transition = transitions
        self.transition_choices = ['fadeOutUp', 'fadeOutDown', 'fadeOut', 'fadeOut', 'fadeOut',
                                   'moveUp', 'moveDown', 'moveLeft', 'moveRight', 'moveUpLeft', 'moveUpRight']
        self.transition.init(self._screen, self.w, self.h)

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
        return self._screen.get_size() if self._screen else self.w, self.h

    @resolution.setter
    def resolution(self, value):
        self.w, self.h = value
        self._screen = pygame.display.set_mode(value)

    def run(self, scene=None):
        if scene is None:
            if self._scene is None:
                raise ValueError('No scene provided')
        else:
            self._scene = scene()
            self._scene.enter()

        context = {
            "delta_time": 0.0,
            "current_time": 0.0,
            "portals": [],
            "other_masks": [],
            "left_top": (0, 0),
            "collision_window": Rect((0, 0), WindowSize).inflate(100, 100),
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

            self.transition.update_screen()

            self.network_connection.pump()
            self.network_client.pump()

            pygame.display.flip()

            memory = process.memory_info().rss
            if memory > 536870912:
                gc.collect()
                logger.debug("内存回收" + str((process.memory_info().rss - memory) / 1024 / 1024) + 'MB')

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

    def change_scene(self, the_scene_class, transition):
        self.transition.init(self._screen, self.w, self.h)
        if not transition:
            transition = random.choice(self.transition_choices)
        self.transition.run(transition, 0.7)
        scene = the_scene_class()
        scene.enter()
        if self._scene:
            self._scene.exit()
            self._scene = None
        self._scene = scene

    def on_change_scene(self, event):
        transition = None
        if hasattr(event, 'transition'):
            transition = event.transition
        self.change_scene(event.scene, transition)

    def on_refresh_scene(self, event):
        print(event.__dict__)
        from game.scene.world.world_scene import WorldScene
        self.change_scene(type(self._scene), None)
        event.handled = True

    def on_changing_screen(self, event):
        pass

    def on_quit(self, event):
        self.running = False
        event.handled = True


director = Director()
