from core.component.component import Component


class MainCharacterComponent(Component):
    def on_receive_path_list(self, event):
        self.state.game_object.target_list = event.path_list
        self.state.game_object.is_new_target = True
        self.state.game_object.is_running = event.is_running
        event.handled = True

    def update(self, data=None):
        data["me_world_pc"] = self.state.game_object.get_xy()
        for portal in data["portals"]:
            if portal.portal_rect.collidepoint(self.state.game_object.get_xy()):
                print(portal, portal.x, portal.y)


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

