import pygame
from pygame.locals import *
from core.ui.state.ui_state import UIState
from settings import ResMargin, logger


class TextInputState(UIState):
    def update(self, context):
        # Update key counters:
        for key in self.game_object.key_repeat_counter:
            self.game_object.key_repeat_counter[key][0] += self.game_object.clock.get_time()  # Update clock
            # Generate new key events if enough time has passed:
            if self.game_object.key_repeat_counter[key][0] >= self.game_object.key_repeat_initial_interval_ms:
                self.game_object.key_repeat_counter[key][0] = (
                        self.game_object.key_repeat_initial_interval_ms
                        - self.game_object.key_repeat_interval_ms)
                event_key, event_unicode = key, self.game_object.key_repeat_counter[key][1]
                if key != 0:
                    pygame.event.post(pygame.event.Event(KEYDOWN, {"key": event_key, "unicode": event_unicode}))

        self.game_object.surface = self.game_object.font_object.render(
            self.game_object.input_string, False, self.game_object.text_color)

        self.game_object.cursor_ms_counter += self.game_object.clock.get_time()
        if self.game_object.cursor_ms_counter >= self.game_object.cursor_switch_ms:
            self.game_object.cursor_ms_counter %= self.game_object.cursor_switch_ms
            self.game_object.cursor_visible = not self.game_object.cursor_visible

        if self.game_object.cursor_visible and self.game_object.focus:
            cursor_y_pos = self.game_object.font_object.size(
                self.game_object.input_string[:self.game_object.cursor_position])[0]
            # Without this, the cursor is invisible when self.cursor_position > 0:
            if self.game_object.cursor_position > 0:
                cursor_y_pos -= self.game_object.cursor_surface.get_width()
            self.game_object.surface.blit(self.game_object.cursor_surface, (cursor_y_pos, 0))

        self.game_object.clock.tick()

    def draw(self, screen):
        origin_rect = self.game_object.surface.get_rect()
        left = max(0, self.game_object.slide_window[0])
        width = min(origin_rect.width, self.game_object.w)
        rect = Rect((left, 0), (width, origin_rect.height))
        sub_surface = self.game_object.surface.subsurface(rect)
        screen.blit(sub_surface, self.game_object.screen_rect)
        del sub_surface
