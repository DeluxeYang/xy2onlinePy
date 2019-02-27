class ColorWrapper:
    def __init__(self, color):
        self.color = color

class EmojiWrapper:
    def __init__(self, wdf, _hash):
        self.wdf = wdf
        self.hash = _hash

class TextWrapper:
    def __init__(self, font_size):
        self.text = ""
        self.len = 0
        self.font_size = font_size

    @staticmethod
    def is_chinese(uchar):
        if len(uchar) != 1:
            raise TypeError('expected a character, but a string found!')
        if u'\u4e00' <= uchar <= u'\u9fa5':
            return True
        else:
            return False

    def append(self, char):
        self.text += char
        self.len += self.font_size if self.is_chinese(char) else self.font_size / 2

    def is_empty(self):
        return True if self.text == "" else False
