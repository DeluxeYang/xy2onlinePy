from core.ui.ui import UI
from utils import ptext

from .ptext_wrapper import PTextWrapper

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

    def translate(self):
        font_num_each_row_max = self.w //self.font_size  #
        self.w = font_num_each_row_max * self.font_size  # 字框重新调整

        text_cache = None
        text_cache_len = 0
        last_x = self.x
        last_y = self.y
        i = 0
        under_matching = False
        last_pattern = None  # color, bold, italic
        ptext_pattern = {"color": None}
        pattern_text_cache = "#"
        while i < len(self.text):
            if self.text[i] == "#":  # 如果是#
                under_matching = True
            elif self.text[i].isalnum():  # 如果是数字或者字母
                if under_matching:
                    pattern_text_cache += self.text[i]
                    if pattern_text_cache in templates:
                        last_pattern = templates[pattern_text_cache]
                    if pattern_text_cache not in prefix:  # 如果前缀不匹配
                        under_matching = False  # 退出匹配模式
                        if last_pattern:  # 有模式
                            if last_pattern[0].endswith("wdf"):  # 表情

                                ptext_instance = PTextWrapper(
                                    text_cache, last_x, last_y,
                                    font_name=self.font_name, font_size=self.font_size,
                                    bold=self.bold, italic=self.italic, underline=self.underline,
                                    color=ptext_pattern.get("color", self.color), background=self.background,
                                    width=self.width, width_em=self.width_em,
                                    line_height=self.line_height, p_space=self.p_space,
                                    strip=self.strip, align=self.align,
                                    o_width=self.o_width, o_color=self.o_color,
                                    shadow=self.shadow, s_color=self.s_color,
                                    g_color=self.g_color, shade=self.shade,
                                    alpha=self.alpha, anchor=self.anchor, angle=self.angle)
                            else:  # 字符样式
                                ptext_pattern[last_pattern[0]] = last_pattern[1]
                        else:  # 无模式
                            text_cache += pattern_text_cache
                            text_cache_len += len(pattern_text_cache)
                        pattern_text_cache = "#"
                        last_pattern = None
                        text_cache_len = 0
                    else:  # 如果匹配则继续
                        continue
                else:
                    text_cache += self.text[i]  # 如果是数字或字母，但不在匹配模式下，则记录到text_cache中
                    text_cache_len += 1
            else:
                if under_matching:
                    under_matching = False  # 退出匹配模式
                    if last_pattern:  # 有模式
                        if isinstance(last_pattern, list):
                            pass  # 断句，生成表情
                        else:
                            ptext_pattern[last_pattern] = True
                    else:  # 无模式
                        text_cache += pattern_text_cache
                        text_cache_len += 1
                    pattern_text_cache = "#"
                    last_pattern = None
                else:
                    text_cache += self.text[i]
                    if self.is_chinese(self.text[i]):  # 如果是中文，则长度+2
                        text_cache_len += 2
                    else:
                        text_cache_len += 1

    @staticmethod
    def is_chinese(uchar):
        if len(uchar) != 1:
            raise TypeError('expected a character, but a string found!')
        if u'\u4e00' <= uchar <= u'\u9fa5':
            return True
        else:
            return False


