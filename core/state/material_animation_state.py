from core.state.animation_state import AnimationState


class MaterialAnimationState(AnimationState):
    res_index = "normal"

    def register(self, obj):
        """
        绑定GameObject
        :param obj:
        :return:
        """
        super().register(obj)
        address = self.game_object.res_info[self.res_index]
        self.res_init(address)  # 初始化res

    def update(self, data):
        one_loop = super().update(data)
        self.set_surface(self.game_object.direction)  # 通常direction为0
        return one_loop

    def draw(self, screen):
        super().draw(screen)  # State的draw 即调用组件draw
        screen.blit(self.game_object.surface, self.game_object.screen_rect)
