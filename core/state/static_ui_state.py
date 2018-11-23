from core.state.state import State
from utils.res_manager import res_manager


class StaticUIState(State):
    res_index = ""

    def __init__(self):
        super().__init__()
        self.res = None

    def register(self, obj):
        super().register(obj)
        address = self.game_object.res_info[self.res_index]
        self.res = res_manager.get_res(address[0], address[1])  # 找到动画资源
        self.game_object.surface = self.res.image_group[0][0]
        self.game_object.inited = True  # 初始化完成
        self.game_object.ready = True

    def draw(self, screen):
        screen.blit(self.game_object.surface, self.game_object.screen_rect)
