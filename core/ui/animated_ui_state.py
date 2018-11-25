from core.state.state import State
from utils.res_manager import res_manager


class AnimatedUIState(State):
    res_index = ""

    def __init__(self):
        super().__init__()
        self.res = None

        self.frame = 0
        self.first_frame = 0
        self.last_frame = 0
        self.last_time = 0

    def register(self, obj):
        super().register(obj)
        address = self.game_object.res_info[self.res_index]
        self.res = res_manager.get_res(address[0], address[1])  # 找到动画资源
        self.game_object.inited = True  # 初始化完成
        self.game_object.ready = True

    def update(self, data):
        one_loop = self.calc_next_frame(data["current_time"], rate=100)  # 计算下一帧的帧数
        self.game_object.surface = self.res.image_group[0][self.frame]
        self.game_object.ready = True
        super().update(data)
        return one_loop

    def draw(self, screen):
        screen.blit(self.game_object.surface, self.game_object.screen_rect)

    def calc_next_frame(self, current_time, rate):
        """
        计算是否移动到下一帧
        :param current_time:
        :param rate:
        :return:
        """
        one_loop = False
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame >= self.last_frame:
                self.frame = self.first_frame
                one_loop = True  # 一次动画循环完毕
            self.last_time = current_time
        return one_loop
