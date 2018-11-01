from .component import Component


class MapMouseComponent(Component):
    def on_mouse_right_down(self, event):
        self.game_object.set_window(self.game_object.get_world_pc(event.pos))
        # self.game_object.find_path(event.pos, is_running=True)

    def on_mouse_left_down(self, event):
        self.game_object.find_path(event.pos, is_running=False)


class MapReceiveComponent(Component):
    def on_receive_map_info(self, event):
        if self.game_object.map_id == event.map_id:
            self.game_object.receive_map_info(event.__dict__)
            event.handled = True

    def on_receive_map_unit(self, event):
        if self.game_object.map_id == event.map_id:
            self.game_object.receive_map_unit(event.__dict__)
            event.handled = True

    def on_receive_path_list(self, event):
        print(event.__dict__)
