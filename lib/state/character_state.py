from pygame.math import Vector2

from .animation import AnimationState
from utils.math import is_same_coordinate, calc_direction_8, calc_direction_4

from settings import RunningSpeed, WalkingSpeed


class CharacterStandNormalState(AnimationState):
    res_index = "stand_normal"

    def __init__(self):
        super().__init__()
        self.loops_count = 0

    def update(self, data):
        one_loop = self._update(data)
        if one_loop:
            self.loops_count += 1
            if self.loops_count >= 3:
                self.game_object.changing_state(CharacterStandTeaseState())


class CharacterStandTeaseState(AnimationState):
    res_index = "stand_tease"

    def update(self, data):
        one_loop = self._update(data)
        if one_loop:
            self.game_object.changing_state(CharacterStandNormalState())


class CharacterMovingState(AnimationState):
    speed = 5

    def update(self, data):
        self._update(data)
        self.calc_next_target()
        if is_same_coordinate(self.game_object.get_xy(), self.game_object.target):  # 如果已经到达目标坐标点
            self.game_object.changing_state(CharacterStandNormalState())
        else:
            self.game_object.direction = calc_direction_8(self.game_object)
            self.move(self.speed)

    def calc_next_target(self):
        if len(self.game_object.target_list) > 0:
            if self.game_object.is_new_target or is_same_coordinate(self.game_object.get_xy(), self.game_object.target):
                self.game_object.is_new_target = False
                self.game_object.target = self.game_object.target_list[0]
                self.game_object.target_list.pop(0)

    def move(self, speed):
        vector = Vector2()
        vector.x = self.game_object.target[0] - self.game_object.x
        vector.y = self.game_object.target[1] - self.game_object.y
        vector.normalize_ip()
        vector.scale_to_length(speed)
        self.game_object.x += vector.x
        self.game_object.y += vector.y

class CharacterWalkingState(CharacterMovingState):
    res_index = "walk"
    speed = WalkingSpeed

class CharacterRunningState(CharacterMovingState):
    res_index = "run"
    speed = RunningSpeed