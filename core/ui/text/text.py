from pygame.locals import *
from core.ui.ui import UI
from core.ui.text.text_state import TextState
from utils import ptext


class Text(UI):
    def __init__(self, text, x=0, y=0, w=0, h=0, ui_id="",
                 font_name="HYC1GJM", font_size=16, sys_font=None,
                 bold=False, italic=False, underline=False,
                 color=ptext.DEFAULT_COLOR, background=ptext.DEFAULT_BACKGROUND,
                 width=None, width_em=None, line_height=ptext.DEFAULT_LINE_HEIGHT,
                 p_space=ptext.DEFAULT_PARAGRAPH_SPACE,
                 align="left", o_width=None, o_color=ptext.DEFAULT_OUTLINE_COLOR,
                 shadow=None, s_color=ptext.DEFAULT_SHADOW_COLOR,
                 g_color=None, shade=ptext.DEFAULT_SHADE,
                 alpha=1.0, anchor=(0.0, 0.0), angle=0):
        super().__init__(None, x, y, w, h, ui_id)
        self.text = text

        self.x = x
        self.y = y

        self.font_name = font_name
        self.font_size = font_size
        self.sys_font = sys_font

        self.bold = bold
        self.italic = italic
        self.underline = underline

        self.color = color
        self.background = background

        self.width = width
        self.width_em = width_em
        self.line_height = line_height
        self.p_space = p_space

        self.align = align

        self.o_width = o_width
        self.o_color = o_color

        self.shadow = shadow
        self.s_color = s_color

        self.g_color = g_color
        self.shade = shade

        self.alpha = alpha
        self.anchor = anchor
        self.angle = angle

        self.init_state(TextState())

    def add_y(self, v):
        self.y += v
        self.screen_rect = Rect((self.x, self.y), (self.w, self.h))
