from pygame.locals import Rect
from pygame.math import Vector2

from base.Font import render_text, blit_text
from base.events import event_manager
from base.animations.Role import Role
from base.interactions.BaseInteractionObject import BaseInteractionObject

from utils.Math import cal_direction_8, is_same_coordinate
from Settings import *

class Player(BaseInteractionObject):
    def __init__(self, data):
        super().__init__()

        self.map_name = data["map_name"]
        self.current = data["current"]
        self.target = self.current
        self.target_list = []
        self.direction = 0
        self.is_running = False
        self.is_new_target = False

        self.role = Role(data["race"],
                         data["version"],
                         data["character_id"])
        self.figure = self.role

        self.level = 8
        self.signals = ["player_moving"]
        self.register()

        self.id = data.get("id", 0)
        self.name = data.get("name", "")
        '''
        self.name = data["name"]
        self.id = data["id"]
        self.title = data["title"]
        self.grade = data["grade"]
        self.experience = data["experience"]

        self.HP_max = data["HP_max"]
        self.HP = data["HP"]
        self.MP_max = data["MP_max"]
        self.MP = data["MP"]
        self.AP = data["AP"]
        self.SP = data["SP"]
        self.speed = data["speed"]
        '''

    def interact(self, event):
        if event.data["player_id"] == self.id:
            if event.signal == "player_moving":
                self.set_target_list(event.data["target_list"])
                self.is_running = event.data["is_running"]
                event.handled = True

    def set_target_list(self, target_list):
        self.is_new_target = True
        self.target_list = target_list

    def set_current(self, current):
        self.current = current
        self.target = self.current
        self.is_new_target = False
        self.target_list = []

    def update(self, data):
        ani = self.render(data)  # 计算动画

        mask = ani.get_mask(self.direction)  # 人物mask
        mask.rect = self.get_rect_of_world(ani)

        highlight = self.mouse_over(data, ani, mask.rect)

        ani.draw(data["window_left_top_pos"], self.current, highlight)

        name, ns = render_text(self.name, (40, 180, 50))
        blit_text(name, ns, data["window_left_top_pos"], self.current, 20)

        # self._detecting_portal(data, ani, mask.rect)
        return mask

    def render(self, data):
        self._moving_to_next_target()  # 判断是否更新到下一个target
        if not is_same_coordinate(self.current, self.target):
            self.direction = cal_direction_8(self)  # 计算方向
            if self.is_running:
                self._move_to_next_pc(Running_Speed)  # 计算下一个当前坐标，地图坐标
                ani = self.figure.run(data["mask_list"], data["window_left_top_pos"],
                                      self.current, self.direction, data["ticks"])
            else:
                self._move_to_next_pc(Walking_Speed)  # 计算下一个当前坐标，地图坐标
                ani = self.figure.walk(data["mask_list"], data["window_left_top_pos"],
                                       self.current, self.direction, data["ticks"])
        else:
            ani = self.figure.stand(data["mask_list"], data["window_left_top_pos"],
                                    self.current, self.direction, data["ticks"])
        return ani

    def mouse_over(self, data, ani, world_rect):
        mouse_mask = data["mouse_mask"]
        left_top = data["window_left_top_pos"]
        sprite_mask = ani.get_mask(self.direction).mask
        offset_x = left_top[0] + mouse_mask.rect.left - world_rect.x
        offset_y = left_top[1] + mouse_mask.rect.top - world_rect.y
        if sprite_mask.overlap(mouse_mask.mask, (offset_x, offset_y)):
            return True
        else:
            return False

    def _detecting_portal(self, data, ani, world_rect):
        portals = data["portal_list"]
        sprite_map_x = world_rect.x
        sprite_map_y = world_rect.y
        sprite_mask = ani.get_mask(self.direction).mask
        for portal in portals:
            offset_x = portal.rect.left - sprite_map_x
            offset_y = portal.rect.top - sprite_map_y
            if sprite_mask.overlap(portal.collision_mask, (offset_x, offset_y)):  # 如果和collision_mask重叠
                continue  # 则判定角色在mask前面，不产生遮挡，跳过
            if sprite_mask.overlap(portal.portal_mask, (offset_x, offset_y)):
                data = {"target_map_id": portal.target_map_id,
                        "target_position": portal.target_position,
                        "me": data["me"]}
                event_manager.emit("transfer", data)  # 向event_manager提交角色移动事件
                break

    def _moving_to_next_target(self):
        if len(self.target_list) > 0:
            if self.is_new_target or is_same_coordinate(self.current, self.target):
                self.is_new_target = False
                self.target = self.target_list[0]
                self.target_list.pop(0)

    def _move_to_next_pc(self, speed):
        vector = Vector2()
        vector.x = self.target[0] - self.current[0]
        vector.y = self.target[1] - self.current[1]
        vector.normalize_ip()
        vector.scale_to_length(speed)
        self.current = self.current[0] + vector.x, self.current[1] + vector.y

    def get_rect_of_world(self, ani):
        x = int(self.current[0]) - Res_Margin - ani.res.x
        y = int(self.current[1]) - Res_Margin - ani.res.y
        w = ani.res.w
        h = ani.res.h
        return Rect(x, y, w, h)

