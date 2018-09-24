import sys
import pygame
from pygame.locals import *
from .Event import Event
from .EventManager import EventManager


event_manager = EventManager()


def event_filter(data):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            pressed_button = pygame.mouse.get_pressed()
            if pressed_button[0]:
                event_manager.emit("mouse_left_down", data)
            if pressed_button[1]:
                print('The mouse wheel Pressed!')
            if pressed_button[2]:
                event_manager.emit("mouse_right_down", data)