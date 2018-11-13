from pygame.math import Vector2

from core.state.animation import AnimationState
from core.state.state import state_factory

from game.character.character_component import CharacterMouseComponent, MainCharacterComponent

from utils.math import is_same_coordinate, calc_direction_8

from settings import RunningSpeed, WalkingSpeed


class CharacterWorldState(AnimationState):
    def is_moving_to_new_target(self, data):
        if self.game_object.is_new_target:  # 有新的移动目的地
            if self.game_object.is_running:
                if self.game_object.is_main_character:
                    _state = state_factory(CharacterRunningState, [MainCharacterComponent, CharacterMouseComponent])
                else:
                    _state = state_factory(CharacterRunningState, [CharacterMouseComponent])
            else:
                if self.game_object.is_main_character:
                    _state = state_factory(CharacterWalkingState, [MainCharacterComponent, CharacterMouseComponent])
                else:
                    _state = state_factory(CharacterWalkingState, [CharacterMouseComponent])
            self.game_object.changing_state(_state, data)  # 则改变状态
            self.game_object.is_new_target = False
            self.game_object.reset_target()
            return True
        return False


class CharacterMovingState(CharacterWorldState):
    speed = 5

    def update(self, data):
        if self.is_moving_to_new_target(data):
            return None
        self.calc_next_target()
        if is_same_coordinate(self.game_object.get_xy(), self.game_object.target):  # 如果已经到达目标坐标点
            if self.game_object.is_main_character:
                _state = state_factory(CharacterStandNormalState, [MainCharacterComponent, CharacterMouseComponent])
            else:
                _state = state_factory(CharacterStandNormalState, [CharacterMouseComponent])
            self.game_object.changing_state(_state, data)
        else:
            self.game_object.direction = calc_direction_8(self.game_object)
            self.move(self.speed)
            super().update(data)

    def calc_next_target(self):
        if len(self.game_object.target_list) > 0:
            if is_same_coordinate(self.game_object.get_xy(), self.game_object.target):
                self.game_object.target = self.game_object.target_list.pop(0)

    def move(self, speed):
        vector = Vector2()
        vector.x = self.game_object.target[0] - self.game_object.x
        vector.y = self.game_object.target[1] - self.game_object.y
        vector.normalize_ip()
        vector.scale_to_length(speed)
        self.game_object.x += vector.x
        self.game_object.y += vector.y


class CharacterStandNormalState(CharacterWorldState):
    res_index = "stand_normal"

    def __init__(self):
        super().__init__()
        self.loops_count = 0

    def update(self, data):
        if self.is_moving_to_new_target(data):
            return
        one_loop = super().update(data)
        if one_loop:
            self.loops_count += 1
            if self.loops_count >= 5:
                if self.game_object.is_main_character:
                    _state = state_factory(CharacterStandTeaseState, [MainCharacterComponent, CharacterMouseComponent])
                else:
                    _state = state_factory(CharacterStandTeaseState, [CharacterMouseComponent])
                self.game_object.changing_state(_state, data)


class CharacterStandTeaseState(CharacterWorldState):
    res_index = "stand_tease"

    def update(self, data):
        if self.is_moving_to_new_target(data):
            return
        one_loop = super().update(data)
        if one_loop:
            if self.game_object.is_main_character:
                _state = state_factory(CharacterStandNormalState, [MainCharacterComponent, CharacterMouseComponent])
            else:
                _state = state_factory(CharacterStandNormalState, [CharacterMouseComponent])
            self.game_object.changing_state(_state, data)


class CharacterWalkingState(CharacterMovingState):
    res_index = "walk"
    speed = WalkingSpeed


class CharacterRunningState(CharacterMovingState):
    res_index = "run"
    speed = RunningSpeed
