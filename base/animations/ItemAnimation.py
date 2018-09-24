from base.animations.Animation import Animation


class ItemAnimation(Animation):
    def __init__(self, address):
        super().__init__(address)

    def update(self, direction, current_time, rate=100):
        """
        动画更新
        :return:
        """
        one_loop = self._cal_next_frame(current_time, rate)
        self._render(direction)
        return one_loop
