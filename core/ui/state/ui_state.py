from utils.res_manager import res_manager


class UIState:
    res_index = ""

    def __init__(self):
        self.game_object = None
        self.res = None

    def register(self, obj):
        self.game_object = obj
        address = self.game_object.res_info[self.res_index]
        self.res = res_manager.get_res(address[0], address[1])  # 找到动画资源
        self.game_object.inited = True  # 初始化完成
        self.game_object.ready = True

    def update(self, data):
        pass

    def draw(self, screen):
        screen.blit(self.game_object.surface, self.game_object.screen_rect)
