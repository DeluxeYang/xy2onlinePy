import pygame
from pygame.locals import Rect
from core.ui.ui import UI
from core.ui.text_input.text_input_base_component import TextInputBaseComponent
from core.ui.text_input.text_input_state import TextInputState


class TextInput(UI):
    def __init__(self, x, y, w, h, input_id,
                 initial_string="", initial_interval_ms=400, interval_ms=35, font_size=18,
                 text_color=(255, 255, 255)):
        super().__init__(None, x, y, w, h)
        self.input_id = input_id
        self.input_string = ""
        self.font_size = font_size

        self.font_object = pygame.font.SysFont("calibri", font_size)
        self.surface = pygame.Surface((1, 1))
        self.surface.set_alpha(0)

        self.slide_window = [0, w]

        self.text_color = text_color

        self.key_repeat_counter = {}
        self.key_repeat_initial_interval_ms = initial_interval_ms
        self.key_repeat_interval_ms = interval_ms

        self.cursor_surface = pygame.Surface((int(self.font_size/20+1), self.font_size))
        self.cursor_surface.fill(text_color)
        self.cursor_position = len(initial_string)  # Inside text
        self.cursor_visible = False  # Switches every self.cursor_switch_ms ms
        self.cursor_switch_ms = 500  #
        self.cursor_ms_counter = 0

        self.clock = pygame.time.Clock()

        self.init_state(TextInputState())
        self.add_component(TextInputBaseComponent())

    def get_surface(self):
        return self.surface

    def get_text(self):
        return self.input_string

    def get_cursor_position(self):
        return self.cursor_position

    def set_text_color(self, color):
        self.text_color = color

    def set_cursor_color(self, color):
        self.cursor_surface.fill(color)

    def clear_text(self):
        self.input_string = ""
        self.cursor_position = 0
