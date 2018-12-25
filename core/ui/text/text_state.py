from core.ui.state.static_ui_state import StaticUIState
from utils import ptext


class TextState(StaticUIState):
    def draw(self, screen):
        x = self.game_object.screen_rect.x
        y = self.game_object.screen_rect.y
        ptext.draw(self.game_object.text, left=x, top=y, fontsize=self.game_object.font_size,
                   fontname=self.game_object.font_name, sysfontname=self.game_object.sys_font,
                   bold=self.game_object.bold, italic=self.game_object.italic, underline=self.game_object.underline,
                   color=self.game_object.color, background=self.game_object.background,
                   width=self.game_object.width, widthem=self.game_object.width_em,
                   lineheight=self.game_object.line_height, pspace=self.game_object.p_space,
                   align=self.game_object.align,
                   owidth=self.game_object.o_width, ocolor=self.game_object.o_color,
                   shadow=self.game_object.shadow, scolor=self.game_object.s_color,
                   gcolor=self.game_object.g_color, shade=self.game_object.shade,
                   alpha=self.game_object.alpha, anchor=self.game_object.anchor, angle=self.game_object.angle)
