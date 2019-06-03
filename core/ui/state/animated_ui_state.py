from core.ui.state.ui_state import UIState
from settings import AnimationRate


class AnimatedUIState(UIState):
    def __init__(self):
        super().__init__()
        self.frame = 0
        self.first_frame = 0
        self.last_frame = 0
        self.last_time = 0

    def update(self, context):
        one_loop = self.calc_next_frame(context["current_time"], rate=AnimationRate)  # 计算下一帧的帧数
        self.game_object.surface = self.res.image_group[0][self.frame]
        self.game_object.ready = True
        return one_loop

    def calc_next_frame(self, current_time, rate):
        """
        计算是否移动到下一帧
        :param current_time:
        :param rate:
        :return:
        """
        if self.res.time_seq:
            rate = self.res.time_seq[self.frame] * rate
        one_loop = False
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame >= self.last_frame:
                self.frame = self.first_frame
                one_loop = True  # 一次动画循环完毕
            self.last_time = current_time
        return one_loop
