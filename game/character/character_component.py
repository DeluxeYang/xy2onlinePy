import pygame
from core.world.director import director
from core.component.component import Component
from settings import logger


class MainCharacterComponent(Component):
    def on_receive_path_list(self, event):
        print(event.__dict__)
        if event.path_list:
            self.state.game_object.target_list = event.path_list
            self.state.game_object.is_new_target = True
            self.state.game_object.is_running = event.is_running
            director.network_client.request(send_data={  # 获取当前主要角色所在场景中的其他玩家
                "action": "moving",
                "account": director.account.account,
                "role_name": director.account.get_main_role().name,
                "map_id": director.account.get_main_role().map_id,
                "path_list": event.path_list,
                "is_running": event.is_running
            })
        event.handled = True


class CharacterMouseComponent(Component):
    def on_mouse_over(self, event):
        if self.is_mouse_focus_on(event):
            self.state.game_object.is_mouse_over = True
            event.handled = True

    def on_mouse_left_down(self, event):
        if self.is_mouse_focus_on(event):
            try:
                if self.state.game_object.name == director.account.get_main_role().name:
                    logger.debug(str(self.state.game_object.x) + ", " + str(self.state.game_object.y))
                director.account.set_main_role(self.state.game_object.id)
            except:
                pass
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

    def on_receive_moving(self, event):
        main_role = director.account.get_main_role()
        if self.state.game_object.id == event.role_id \
                and event.map_version == main_role.map_version \
                and event.map_id == main_role.map_id \
                and event.except_account != director.account.account:
            self.state.game_object.target_list = event.path_list
            self.state.game_object.is_new_target = True
            self.state.game_object.is_running = event.is_running
            event.handled = True

    # def draw(self, screen=None):
    #     pygame.draw.rect(screen, (0, 0, 0), self.state.game_object.screen_rect)

