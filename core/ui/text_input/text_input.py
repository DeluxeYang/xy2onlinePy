import pygame
# from pygame.locals import *
from core.ui.ui import UI
from core.ui.textfield.textfield import TextField


class TextInput(UI):
    def __init__(self, x, y, w, h,
                 initial_string="", initial_interval_ms=400, interval_ms=35, font_size=16):
        super().__init__(None, x, y, w, h)
        self.input_string = ""
        self.text_field = TextField(self.input_string, x, y, w, h,
                                    font_size=font_size, font_name=None, sys_font="simsunnsimsun")

        self.font_size = font_size
        self.key_repeat_counter = {}
        self.key_repeat_initial_interval_ms = initial_interval_ms
        self.key_repeat_interval_ms = interval_ms

        self.cursor_surface = pygame.Surface((int(self.font_size/20+1), self.font_size))
        self.cursor_surface.fill((0, 0, 1))
        self.cursor_position = len(initial_string)  # Inside text
        self.cursor_visible = True  # Switches every self.cursor_switch_ms ms
        self.cursor_switch_ms = 500  #
        self.cursor_ms_counter = 0

        self.clock = pygame.time.Clock()

    def remove_children(self):
        for child in self.children:
            child.destroy()
        self.children = []

    def update_text_field(self):
        self.text_field = TextField(self.text, self.x, self.y, self.w, self.h,
                                    font_name=None, sys_font="simsunnsimsun")
        self.add_child(self.text_field)
