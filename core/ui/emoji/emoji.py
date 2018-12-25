from core.ui.ui import UI
from core.ui.emoji.emoji_state import EmojiState


class Emoji(UI):
    def __init__(self, res_info, x=0, y=0, w=0, h=0):
        super().__init__(res_info, x, y, w, h)
        self.init_state(EmojiState())


def emoji_factory(res_tuple, x, y):
    res_info = {"normal": res_tuple}
    return Emoji(res_info, x, y)
