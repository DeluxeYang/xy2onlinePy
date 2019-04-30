from core.component.component import Component
from core.world.director import director
from core.event.event import post_event


class MapMouseComponent(Component):
    def on_mouse_right_down(self, event):
        self._find_path(event, is_running=True)
        event.handled = True

    def on_mouse_left_down(self, event):
        self._find_path(event, is_running=False)
        event.handled = True

    def _find_path(self, event, is_running):
        left_top = self.state.game_object.get_left_top()  # screen左上角世界坐标
        source = director.account.get_main_role().get_xy()  # main_role当前坐标
        target = (event.pos[0] + left_top[0], event.pos[1] + left_top[1])  # screen左上角世界坐标 + screen鼠标位置 = 鼠标世界坐标
        path_list = self.state.game_object.map_x.find_path(source, target)
        post_event({
            'name': "receive_path_list",
            'path_list': path_list,
            'is_running': is_running})
