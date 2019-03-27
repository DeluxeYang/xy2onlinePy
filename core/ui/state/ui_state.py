from utils.res_manager import res_manager
from settings import ResMargin, logger


class UIState:
    res_index = ""

    def __init__(self):
        self.game_object = None
        self.res = None
        self.last_frame = 0

    def register(self, obj):
        self.game_object = obj
        self.binding_res()
        self.game_object.inited = True  # 初始化完成
        self.game_object.ready = True

    def binding_res(self):
        if self.game_object.res_info:
            address = self.game_object.res_info[self.res_index]
            self.res = res_manager.get_res(address[0], address[1])  # 找到动画资源
            self.last_frame = self.res.frame_num
            logger.debug("res_info："+str(self.game_object.res_info)+"，宽："+str(self.res.w)+"，高："+str(self.res.h))

    def update(self, context):
        pass

    def draw(self, screen):
        temp_rect = self.game_object.screen_rect.move(-ResMargin, -ResMargin)
        screen.blit(self.game_object.surface, temp_rect)

    def enter(self):
        pass

    def exit(self):
        self.destroy()

    def destroy(self):
        self.game_object = None
        self.res = None
        del self
