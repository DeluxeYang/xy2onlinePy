from core.ui.ui import UI
from utils import ptext

template = {
    "#r": ["color", "red"], "#g": ["color", "green"], "#b": ["color", "blue"],
    "#p": ["color", "pink"], "#P": ["color", "purple"], "#B": ["color", "black"],
    "#y": ["color", "yellow"], "#o": ["color", "orange"],
    "# ": ["color", "pink"],
}


class TextField(UI):
    def __init__(self, text, res_info, x, y, w, h,
                 font_name="HYC1GJM", font_size=24,
                 bold=False, italic=False, underline=False,
                 color=ptext.DEFAULT_COLOR, background=ptext.DEFAULT_BACKGROUND,
                 width=None, width_em=None, line_height=ptext.DEFAULT_LINE_HEIGHT, p_space=ptext.DEFAULT_PARAGRAPH_SPACE,
                 align="left", o_width=None, o_color=ptext.DEFAULT_OUTLINE_COLOR,
                 shadow=None, s_color=ptext.DEFAULT_SHADOW_COLOR,
                 g_color=None, shade=ptext.DEFAULT_SHADE,
                 alpha=1.0, anchor=(0.0, 0.0), angle=0, strip=True):
        super().__init__(res_info, x, y, w, h)
        self.text = text
        self.content = []

        self.font_name = font_name
        self.font_size = font_size

        self.bold = bold
        self.italic = italic
        self.underline = underline

        self.color = color
        self.background = background

        self.width = width
        self.width_em = width_em
        self.line_height = line_height
        self.p_space = p_space

        self.strip = strip
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

    def translate(self):
        pass