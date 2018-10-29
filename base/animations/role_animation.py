from base.animations.animation import Animation


class RoleAnimation(Animation):
    def __init__(self, address):
        super().__init__(address)

    def update(self, other_masks, world_pc, direction, current_time, rate=100):
        """
        动画更新
        :return:
        """
        one_loop = self._cal_next_frame(current_time, rate)
        self._render(direction, other_masks, world_pc)
        return one_loop

    def update_loop(self, other_masks, world_pc, direction, current_time, rate=100):
        """
        动画帧来回更新
        """
        one_loop = self._cal_next_frame_in_loop(current_time, rate)
        self._render(direction, other_masks, world_pc)
        return one_loop
