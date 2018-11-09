from pygame.math import Vector2

from core.component.component import Component
from core.state.animation import AnimationState
from core.state.state import state_factory

from utils.math import is_same_coordinate, calc_direction_8, calc_direction_4

from settings import RunningSpeed, WalkingSpeed


class CharacterStandNormalState(AnimationState):
    res_index = "stand_normal"

    def __init__(self):
        super().__init__()
        self.loops_count = 0

    def update(self, data):
        one_loop = super().update(data)
        if one_loop:
            self.loops_count += 1
            if self.loops_count >= 3:
                if self.game_object.is_main_character:
                    _state = state_factory(CharacterStandTeaseState, [MainCharacterComponent, CharacterMouseComponent])
                else:
                    _state = state_factory(CharacterStandTeaseState, [CharacterMouseComponent])
                self.game_object.changing_state(_state, data)


class CharacterStandTeaseState(AnimationState):
    res_index = "stand_tease"

    def update(self, data):
        one_loop = super().update(data)
        if one_loop:
            if self.game_object.is_main_character:
                _state = state_factory(CharacterStandNormalState, [MainCharacterComponent, CharacterMouseComponent])
            else:
                _state = state_factory(CharacterStandNormalState, [CharacterMouseComponent])
            self.game_object.changing_state(_state, data)


class CharacterMovingState(AnimationState):
    speed = 5

    def update(self, data):
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
            if self.game_object.is_new_target or is_same_coordinate(self.game_object.get_xy(), self.game_object.target):
                self.game_object.is_new_target = False
                self.game_object.target = self.game_object.target_list.pop(0)

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


class MainCharacterComponent(Component):
    def on_receive_path_list(self, event):
        self.state.game_object.target_list = event.path_list
        self.state.game_object.is_new_target = True
        self.state.game_object.is_running = event.is_running
        if self.state.game_object.is_running:
            _state = state_factory(CharacterRunningState, [MainCharacterComponent, CharacterMouseComponent])
        else:
            _state = state_factory(CharacterWalkingState, [MainCharacterComponent, CharacterMouseComponent])
        self.state.game_object.changing_state(_state)
        event.handled = True


class CharacterMouseComponent(Component):
    def on_mouse_over(self, event):
        if self.is_mouse_focus_on(event):
            self.state.game_object.is_mouse_over = True
            event.handled = True

    def on_mouse_left_down(self, event):
        if self.is_mouse_focus_on(event):
            print(self.state.game_object.character_id)
            event.handled = True

    def on_mouse_right_down(self, event):
        if self.is_mouse_focus_on(event):
            event.handled = True

    def is_mouse_focus_on(self, event):
        if self.state.game_object.screen_rect.collidepoint(event.pos):
            offset_x = event.mouse_point_mask.rect.left - self.state.game_object.screen_rect.left
            offset_y = event.mouse_point_mask.rect.top - self.state.game_object.screen_rect.top
            if self.state.game_object.mask.mask.overlap(event.mouse_point_mask.mask, (offset_x, offset_y)):
                return True
        return False

    # def draw(self, screen=None):
    #     pygame.draw.rect(screen, (0, 0, 0), self.state.game_object.screen_rect)

