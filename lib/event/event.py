import pygame
from pygame.locals import *

from utils.mask import Mask

mouse_mask = pygame.Mask((2, 2))
mouse_mask.fill()


class Event:
    def __init__(self, data):
        if "name" not in data:
            raise KeyError("Event must have a 'name'.")
        for key, value in data.items():
            self.__setattr__(key, value)
        self.handled = False

    def set_attr(self, name, value):
        self.__setattr__(name, value)


def post_event(data_dict):
    event = pygame.event.Event(USEREVENT, data_dict)
    pygame.event.post(event)


def get_mouse_point_mask(mouse_pos):
    mouse_rect = Rect(mouse_pos[0], mouse_pos[1], 2, 2)
    return Mask(mouse_rect, mouse_mask)


def event_filter():
    mouse_pos = pygame.mouse.get_pos()
    mouse_point_mask = get_mouse_point_mask(mouse_pos)

    event_queue = [Event({"name": "mouse_over", "pos": mouse_pos, "mouse_point_mask": mouse_point_mask})]  # 预置一个mouse_over事件

    for event in pygame.event.get():
        event_attributes = event.__dict__
        if event.type in my_events:
            temp = my_events[event.type]
            if isinstance(temp, dict):  # 如果有二级列表
                if event_attributes["button"] not in temp:
                    continue
                event_attributes["name"] = temp[event_attributes["button"]]
                event_attributes["mouse_point_mask"] = mouse_point_mask
            else:
                event_attributes["name"] = temp
            event_queue.append(Event(event_attributes))
        elif event.type == USEREVENT:
            event_queue.append(Event(event_attributes))
    return event_queue


my_events = {
    12: "quit",
    5: {
        1: "mouse_left_down",  # MOUSE BUTTON DOWN = 5
        2: "mouse_mid_down",
        3: "mouse_right_down",
        4: "mouse_wheel_forward_down",
        5: "mouse_wheel_backward_down"
    },
    6: {
        1: "mouse_left_up",  # MOUSE BUTTON UP = 6
        2: "mouse_mid_up",
        3: "mouse_right_up",
    },
    4: "mouse_motion"
}