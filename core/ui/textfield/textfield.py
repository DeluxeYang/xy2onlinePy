from core.ui.ui import UI
from utils import ptext

from .ptext_wrapper import PTextWrapper, ColorWrapper, EmojiWrapper, TextWrapper
from .emoji import emoji_factory, Emoji

templates = {
    "#red": ["color", "red"],
    "#24": ["gires2.wdf", "0x12345678"]
}

prefix = {
    "#": 1,
    "#r": 1, "#re": 1,
    "#2": 1
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

    def translate_and_split(self):
        contents = []
        i = 0
        pattern_matching = False
        last_pattern = None  # color, bold, italic
        pattern_text_cache = "#"
        while i < len(self.text):
            if self.text[i] == "#":  # 如果是#
                pattern_matching = True
            elif self.text[i].isalnum():  # 如果是数字或者字母
                if pattern_matching:  # 如果此时正在匹配
                    pattern_text_cache += self.text[i]  # 则暂存该字符
                    if pattern_text_cache in templates:  # 如果有该模式
                        last_pattern = templates[pattern_text_cache]  # 记录
                    if pattern_text_cache not in prefix:  # 如果前缀不匹配
                        pattern_matching = False  # 退出匹配模式
                        if last_pattern:
                            contents.append(self.pattern_transform(last_pattern))
                        else:
                            for x in pattern_text_cache:
                                contents.append(x)
                        last_pattern = None
                        pattern_text_cache = "#"
                else:
                    contents.append(self.text[i])
            else:
                if pattern_matching:
                    pattern_matching = False  # 退出匹配模式
                    if last_pattern:
                        contents.append(self.pattern_transform(last_pattern))
                    else:
                        for x in pattern_text_cache:
                            contents.append(x)
                    last_pattern = None
                    pattern_text_cache = "#"
                contents.append(self.text[i])
            i += 1
        if last_pattern:
            contents.append(self.pattern_transform(last_pattern))
        elif pattern_text_cache != "#":
            for x in pattern_text_cache:
                contents.append(x)
        return contents

    def rebuild(self, contents):
        # p_text_instance = self.generate_p_text(text="", x=self.x, y=self.y)

        temp_text = TextWrapper()
        p_text_state = {
            "color": self.color
        }
        temp_x = 0
        temp_y = 0
        temp_line_height = self.line_height
        for content in contents:
            if isinstance(content, EmojiWrapper):
                pass  #  TODO 结算
            elif isinstance(content, ColorWrapper):
                p_text_state["color"] = content.color
                if not temp_text.is_empty():
                    pass  #  TODO 结算
            else:
                temp_text.append(content)
            if temp_text.len + temp_x >= self.w:
                pass  # TODO 结算


    def generate_p_text(self, text, x, y):
        p_text_instance = PTextWrapper(text=text, x=x, y=y, font_name=self.font_name, font_size=self.font_size,
                                       bold=self.bold, italic=self.italic, underline=self.underline,
                                       color=self.color, background=self.background,
                                       width=self.width, width_em=self.width_em, line_height=self.line_height,
                                       p_space=self.p_space,
                                       align=self.align, o_width=self.o_width, o_color=self.o_color,
                                       shadow=self.shadow, s_color=self.s_color,
                                       g_color=self.g_color, shade=self.shade,
                                       alpha=self.alpha, anchor=self.anchor, angle=self.angle, strip=self.strip)
        return p_text_instance

    @staticmethod
    def pattern_transform(pattern):
        if pattern[0] == "color":
            return ColorWrapper(pattern[1])
        else:
            return EmojiWrapper(pattern[0], pattern[1])

    @staticmethod
    def is_chinese(uchar):
        if len(uchar) != 1:
            raise TypeError('expected a character, but a string found!')
        if u'\u4e00' <= uchar <= u'\u9fa5':
            return True
        else:
            return False
