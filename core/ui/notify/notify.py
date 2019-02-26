import pygame
from pygame.locals import Rect
from settings import ResMargin
from core.ui.ui import UI
from core.ui.text_field.text_field import TextField
from core.ui.notify.notify_state import NotifyState
from core.ui.notify.notify_base_component import NotifyMouseComponent


class Notify(UI):
    def __init__(self, res_info, text, x, y, w=280, h=60, ui_id="",
                 font_name=None, font_size=12, sys_font="simsunnsimsun",
                 default_color="#FFFF00", focus_color="#008800"):
        super().__init__(res_info, x, y, w, h, ui_id)
        self.text = text

        self.font_name = font_name
        self.font_size = font_size
        self.sys_font = sys_font
        self.default_color = default_color
        self.focus_color = focus_color

        text_field = TextField(
            self.text, 0, 0, 240, self.h,
            font_name=self.font_name, font_size=self.font_size,
            sys_font=self.sys_font, color=self.default_color)

        self.add_child(text_field)

        self.init_state(NotifyState())
        self.add_component(NotifyMouseComponent())

        horizon_mul = 12
        vertical_mul = 1 if text_field.total_height <= self.font_size + 12 else text_field.total_height // 20 + 1

        self.modify_surface(horizon_mul, vertical_mul)

        text_field.x = (40+20*horizon_mul)//2 - text_field.total_width//2
        text_field.y = 8 if text_field.line_has_emoji else 20

    def modify_surface(self, horizon_mul, vertical_mul):
        left_top = self.surface.subsurface(Rect((ResMargin, ResMargin), (20, 20)))
        mid_top = self.surface.subsurface(Rect((20 + ResMargin, ResMargin), (20, 20)))
        right_top = self.surface.subsurface(Rect((40 + ResMargin, ResMargin), (20, 20)))

        left = self.surface.subsurface(Rect((ResMargin, 20 + ResMargin), (20, 20)))
        mid = self.surface.subsurface(Rect((20 + ResMargin, 20 + ResMargin), (20, 20)))
        right = self.surface.subsurface(Rect((40 + ResMargin, 20 + ResMargin), (20, 20)))

        left_bottom = self.surface.subsurface(Rect((ResMargin, 40 + ResMargin), (20, 20)))
        mid_bottom = self.surface.subsurface(Rect((20 + ResMargin, 40 + ResMargin), (20, 20)))
        right_bottom = self.surface.subsurface(Rect((40 + ResMargin, 40 + ResMargin), (20, 20)))

        temp_surface = pygame.Surface(
            (40 + 20 * horizon_mul + ResMargin * 2, 40 + 20 * vertical_mul + ResMargin * 2), pygame.SRCALPHA)

        for i in range(vertical_mul + 2):
            for j in range(horizon_mul + 2):
                if i == 0:
                    if j == 0:
                        temp_surface.blit(left_top, (20 * j + ResMargin, 20 * i + ResMargin))
                    elif j == horizon_mul + 1:
                        temp_surface.blit(right_top, (20 * j + ResMargin, 20 * i + ResMargin))
                    else:
                        temp_surface.blit(mid_top, (20 * j + ResMargin, 20 * i + ResMargin))
                elif i == vertical_mul + 1:
                    if j == 0:
                        temp_surface.blit(left_bottom, (20 * j + ResMargin, 20 * i + ResMargin))
                    elif j == horizon_mul + 1:
                        temp_surface.blit(right_bottom, (20 * j + ResMargin, 20 * i + ResMargin))
                    else:
                        temp_surface.blit(mid_bottom, (20 * j + ResMargin, 20 * i + ResMargin))
                else:
                    if j == 0:
                        temp_surface.blit(left, (20 * j + ResMargin, 20 * i + ResMargin))
                    elif j == horizon_mul + 1:
                        temp_surface.blit(right, (20 * j + ResMargin, 20 * i + ResMargin))
                    else:
                        temp_surface.blit(mid, (20 * j + ResMargin, 20 * i + ResMargin))
        self.surface = temp_surface
        self.h = (vertical_mul + 2) * 20
        self.w = (horizon_mul + 2) * 20
