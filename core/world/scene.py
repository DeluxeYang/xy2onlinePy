from core.world.director import director
from core.world.layer import MapLayer, UILayer
from core.entity.static_object import static_object_factory
from core.entity.material_animation_object import material_animation_object_factory

from core.ui.frame.frame import FixedFrame
from core.ui.button.button import Button


class Scene:
    scene_init_data = None

    def __init__(self):
        self.director = director
        self.layers = []  # layer层，其z序固定，由近及远，z越大则越远

        self.title = self.scene_init_data["title"]
        self.resolution = self.scene_init_data["resolution"]

        # MapLayer
        welcome_map_layer = MapLayer()
        for game_object in self.scene_init_data["layers"]["map"]:
            if game_object["type"] == "static":
                obj = static_object_factory(game_object["res_info"],
                                            game_object["world_position"][0], game_object["world_position"][1])
                welcome_map_layer.add_game_object(obj)
            elif game_object["type"] == "material_animation":
                obj = material_animation_object_factory(game_object["res_info"],
                                                        game_object["world_position"][0],
                                                        game_object["world_position"][1])
                welcome_map_layer.add_game_object(obj)

        # UILayer
        ui_layer = UILayer()
        for frame in self.scene_init_data["layers"]["ui"]:
            if frame["type"] == "fixed":
                frame_instance = FixedFrame(res_info=frame["res_info"],
                                            x=frame["screen_position"][0], y=frame["screen_position"][1],
                                            w=frame["w"], h=frame["h"])
                for factor in frame["factor"]:
                    if factor["type"] == "button":
                        button_instance = Button(res_info=factor["res_info"],
                                                 x=factor["relative_position"][0], y=factor["relative_position"][1],
                                                 w=factor["w"], h=factor["h"])
                        for c in factor["components"]:
                            button_instance.add_component(c)
                        frame_instance.add_child(button_instance)
                ui_layer.add_game_object(frame_instance)

        # Layer Adding
        self.add_layer(ui_layer)
        self.add_layer(welcome_map_layer)

    def handle_event(self, event):
        if hasattr(self, "on_" + event.name):  # 如果self有该事件的处理方法
            getattr(self, "on_" + event.name)(event)  # 则处理
        if not event.handled:  # 如果该事件没有被handle & obj对象有Children属性
            for layer in self.layers:  # 则循环遍历每个layer
                layer.handle_event(event)  # 调用其handle_event方法
                if event.handled:  # 如果被handle则退出
                    break
    """
    layer 更新流
        event   early   update  late    draw
        
    ui    \      \         /     \        /
    shape  \      \       /       \      /
    map     \      \     /         \    / 
    """
    def update(self, data):
        for layer in self.layers:  # 遍历每个layer  early_update
            layer.early_update(data)
        for layer in self.layers[::-1]:  # 遍历每个layer  update
            layer.update(data)
        for layer in self.layers:  # 遍历每个layer  late_update
            layer.late_update(data)

    def draw(self, screen):
        for layer in self.layers[::-1]:  # 逆序遍历每个layer
            layer.draw(screen)

    def add_layer(self, layer):
        self.layers.append(layer)

    def enter(self):
        director.title = self.title
        director.resolution = self.resolution

    def exit(self):
        pass
