from .component import Component


class MapMouseComponent(Component):
    def on_mouse_right_down(self, event):
        self.game_object.find_path(event.pos, is_running=True)

    def on_mouse_left_down(self, event):
        self.game_object.find_path(event.pos, is_running=False)


class MapReceiveComponent(Component):
    def on_receive_map_info(self, event):
        pass

    def on_receive_map_unit(self, event):
        pass

