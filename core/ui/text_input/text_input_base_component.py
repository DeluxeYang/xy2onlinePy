from core.ui.ui_mouse_component import UIMouseComponent
from pygame.locals import *


class TextInputBaseComponent(UIMouseComponent):
    def on_key_down(self, event):
        self.game_object.cursor_visible = True
        if event.key not in self.game_object.key_repeat_counter:
            self.game_object.key_repeat_counter[event.key] = [0, event.unicode]

        if event.key == K_BACKSPACE:
            self.game_object.input_string = (
                    self.game_object.input_string[:max(self.game_object.cursor_position - 1, 0)]
                    + self.game_object.input_string[self.game_object.cursor_position:]
            )
            self.game_object.cursor_position = max(self.game_object.cursor_position - 1, 0)
        elif event.key == K_DELETE:
            self.game_object.input_string = (
                    self.game_object.input_string[:self.game_object.cursor_position]
                    + self.game_object.input_string[self.game_object.cursor_position + 1:]
            )
        elif event.key == K_RIGHT:
            # Add one to cursor_pos, but do not exceed len(input_string)
            self.game_object.cursor_position = min(self.game_object.cursor_position + 1,
                                                   len(self.game_object.input_string))
        elif event.key == K_LEFT:
            # Subtract one from cursor_pos, but do not go below zero:
            self.game_object.cursor_position = max(self.game_object.cursor_position - 1, 0)

        elif event.key == K_END:
            self.game_object.cursor_position = len(self.game_object.input_string)

        elif event.key == K_HOME:
            self.game_object.cursor_position = 0

        else:
            # If no special key is pressed, add unicode of key to input_string
            self.game_object.input_string = (
                    self.game_object.input_string[:self.game_object.cursor_position]
                    + event.unicode
                    + self.game_object.input_string[self.game_object.cursor_position:]
            )
            self.game_object.cursor_position += len(event.unicode)  # Some are empty, e.g. K_UP
        event.handled = True
        print(self.game_object.input_string)

    def on_key_up(self, event):
        if event.key in self.game_object.key_repeat_counter:
            del self.game_object.key_repeat_counter[event.key]
        event.handled = True

    def on_mouse_left_down(self, event):
        if self.is_mouse_in_rect(event):
            self.game_object.set_focus()
            event.handled = True
