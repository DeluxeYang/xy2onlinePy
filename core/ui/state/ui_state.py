from utils.res_manager import res_manager
from settings import ResMargin


class UIState:
    res_index = ""

    def __init__(self):
        self.game_object = None
        self.res = None
        self.last_frame = 0

    def register(self, obj):
        self.game_object = obj
        if self.game_object.res_info:
            address = self.game_object.res_info[self.res_index]
            self.res = res_manager.get_res(address[0], address[1])  # 找到动画资源
            self.last_frame = self.res.frame_num
            print(self.res.w, self.res.h)  # TODO DEBUG
        self.game_object.inited = True  # 初始化完成
        self.game_object.ready = True

    def update(self, context):
        pass

    def draw(self, screen):
        temp_rect = self.game_object.screen_rect.move(-ResMargin, -ResMargin)
        screen.blit(self.game_object.surface, temp_rect)

    def enter(self):
        pass

    def exit(self):
        pass

    def destroy(self):
        del self
