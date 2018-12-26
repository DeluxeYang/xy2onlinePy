from core.ui.ui import UI
from utils import ptext

from core.ui.textfield.textfield_state import TextFieldState
from core.ui.text.text import Text
from core.ui.textfield.wrappers import ColorWrapper, EmojiWrapper, TextWrapper
from core.ui.emoji.emoji import emoji_factory

templates = {
    "#red": ["color", "red"],
    "#tan": ["color", "tan"],
    "#sky": ["color", "deepskyblue"],
    "#blue": ["color", "blue"],
    "#pink": ["color", "pink"],
    "#gold": ["color", "goldenrod2"],
    "#grey": ["color", "grey"],
    "#white": ["color", "white"],
    "#green": ["color", "green"],
    "#brown": ["color", "brown"],
    "#black": ["color", "black"],
    "#yellow": ["color", "yellow"],
    "#purple": ["color", "purple"],
    "#orange": ["color", "orange"],

    "#24": ["gires.wdf", "0x1A7FADBF"]
}

prefix = {
    "#": 1,
    "#r": 1, "#re": 1,
    "#s": 1, "#sk": 1,
    "#t": 1, "#ta": 1,
    "#w": 1, "#wh": 1, "#whi": 1, "#whit": 1,
    "#y": 1, "#ye": 1, "#yel": 1, "#yell": 1, "#yello": 1,
    "#o": 1, "#or": 1, "#ora": 1, "#oran": 1, "#orang": 1,
    "#g": 1, "#gr": 1, "#gre": 1, "#gree": 1, "#go": 1, "#gol": 1,
    "#p": 1, "#pi": 1, "#pin": 1, "#pu": 1, "#pur": 1, "#purp": 1, "#purpl": 1,
    "#b": 1, "#bl": 1, "#blu": 1, "#blue": 1, "#br": 1, "#bro": 1, "#brow": 1, "#bla": 1, "#blac": 1,
    "#1": 1, "#2": 1, "#3": 1, "#4": 1, "#5": 1,
    "#6": 1, "#7": 1, "#8": 1, "#9": 1, "#10": 1,
}


class TextField(UI):
    def __init__(self, text, res_info, x, y, w, h,
                 font_name="HYF2GJM", font_size=16, sys_font=None,
                 bold=False, italic=False, underline=False,
                 color=ptext.DEFAULT_COLOR, background=ptext.DEFAULT_BACKGROUND,
                 width=None, width_em=None, line_height=16, p_space=ptext.DEFAULT_PARAGRAPH_SPACE,
                 align="left", o_width=None, o_color=ptext.DEFAULT_OUTLINE_COLOR,
                 shadow=None, s_color=ptext.DEFAULT_SHADOW_COLOR,
                 g_color=None, shade=ptext.DEFAULT_SHADE,
                 alpha=1.0, anchor=(0.0, 0.0), angle=0, strip=True):
        super().__init__(res_info, x, y, w, h)
        self.text = text

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

        contents = self.translate_and_split()
        self.rebuild(contents)

        self.init_state(TextFieldState())

    def translate_and_split(self):
        """
        将text中的表情等元素解析出来，并打散成列表
        :return:
        """
        contents = []
        i = 0
        pattern_matching = False
        last_pattern = None  # color, bold, italic
        pattern_text_cache = "#"
        while i < len(self.text):
            if self.text[i] == "#":  # 如果是#
                pattern_matching = True
            elif self.text[i].encode('UTF-8').isalnum():  # 如果是数字或者字母
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
        """
        将translate_and_split生成的列表中元素，组成成Emoji、Text，并且断行断句
        :param contents:
        :return:
        """
        temp_text = TextWrapper(self.font_size)
        p_text_state = self.generate_text_state()
        temp_x = 0
        temp_y = 0
        line_height_correcter = {}
        i = 0
        line_num = 1
        emoji_flag = False
        for content in contents:
            if isinstance(content, EmojiWrapper):
                if not temp_text.is_empty():
                    text_instance = Text(text=temp_text.text, x=temp_x, y=temp_y, **p_text_state)
                    self.add_child(text_instance)  # 添加表情
                    i += 1
                    temp_x += temp_text.len
                    temp_text = TextWrapper(self.font_size)
                emoji_instance = emoji_factory([content.wdf, content.hash], temp_x, temp_y)  # 生成表情
                self.add_child(emoji_instance)  # 添加表情
                i += 1
                temp_x += emoji_instance.state.res.w  # 根据表情宽度更改位置
                emoji_flag = True
                line_height_correcter[line_num] = emoji_flag, i
            elif isinstance(content, ColorWrapper):
                if not temp_text.is_empty():
                    text_instance = Text(text=temp_text.text, x=temp_x, y=temp_y, **p_text_state)
                    self.add_child(text_instance)  # 添加表情
                    i += 1
                    temp_x += temp_text.len
                    temp_text = TextWrapper(self.font_size)
                p_text_state["color"] = content.color
            else:
                temp_text.append(content)
            if temp_text.len + temp_x + self.font_size >= self.w:
                if not temp_text.is_empty():
                    text_instance = Text(text=temp_text.text, x=temp_x, y=temp_y, **p_text_state)
                    self.add_child(text_instance)  # 添加表情
                    i += 1
                temp_x = 0
                temp_y += self.font_size + self.line_height if emoji_flag else self.font_size + 5  # 下一行的距离
                temp_text = TextWrapper(self.font_size)
                line_height_correcter[line_num] = emoji_flag, i
                line_num += 1
                emoji_flag = False
        if not temp_text.is_empty():
            text_instance = Text(text=temp_text.text, x=temp_x, y=temp_y, **p_text_state)
            self.add_child(text_instance)  # 添加表情
            i += 1
            line_height_correcter[line_num] = emoji_flag, i
        i = 0
        for line_number in range(1, line_num+1):  # 根据每一行是否有表情，重新定位每一行的行距
            correcter = line_height_correcter[line_number]
            if correcter[0]:
                for ii in range(i, correcter[1]):
                    if isinstance(self.children[ii], Text):
                        self.children[ii].add_y(12)
            i = correcter[1]

    def generate_text_state(self):
        text_state = {
            "font_name": self.font_name, "font_size": self.font_size, "sys_font": self.sys_font,
            "bold": self.bold, "italic": self.italic, "underline": self.underline,
            "color": self.color, "background": self.background,
            "width": self.width, "width_em": self.width_em, "line_height": self.line_height,
            "p_space": self.p_space,
            "align": self.align, "o_width": self.o_width, "o_color": self.o_color,
            "shadow": self.shadow, "s_color": self.s_color,
            "g_color": self.g_color, "shade": self.shade,
            "alpha": self.alpha, "anchor": self.anchor, "angle": self.angle
        }
        return text_state

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
