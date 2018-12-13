from core.ui.state.ui_state import UIState
from utils import ptext


class TextFieldState(UIState):
    def register(self, obj):
        self.game_object = obj
        self.game_object.inited = True
        self.game_object.ready = True

    def draw(self, screen):
        ptext.draw(self.game_object.text, left=self.game_object.x, top=self.game_object.y,
                   fontname=self.game_object.font_name, fontsize=self.game_object.font_size,
                   bold=self.game_object.bold, italic=self.game_object.italic, underline=self.game_object.underline,
                   color=self.game_object.color, background=self.game_object.background,
                   width=self.game_object.width, widthem=self.game_object.width_em,
                   lineheight=self.game_object.line_height, pspace=self.game_object.p_space,
                   strip=self.game_object.strip, align=self.game_object.align,
                   owidth=self.game_object.o_width, ocolor=self.game_object.o_color,
                   shadow=self.game_object.shadow, scolor=self.game_object.s_color,
                   gcolor=self.game_object.g_color, shade=self.game_object.shade,
                   alpha=self.game_object.alpha, anchor=self.game_object.anchor, angle=self.game_object.angle)
