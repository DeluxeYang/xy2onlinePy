from core.world.director import director
from core.world.layer import MapLayer, UILayer, ShapeLayer

from core.entity.static_object import static_object_factory
from core.entity.material_animation_object import material_animation_object_factory

from core.ui.frame.frame import FixedFrame
from core.ui.button.button import Button
from core.ui.text_field.text_field import TextField
from core.ui.text_input.text_input import TextInput

from game.map.map import Map


class Scene:
    scene_init_data = None

    def __init__(self):
        self.director = director
        self.ui_layer = None
        self.shape_layer = None
        self.map_layer = None

        self.layers = []  # layer层，其z序固定，由近及远，z越大则越远

        self.title = self.scene_init_data["title"]
        self.resolution = self.scene_init_data["resolution"]

        # MapLayer
        self.map_layer = MapLayer()
        for game_object in self.scene_init_data["layers"]["map"]:
            if game_object["type"] == "static":
                obj = static_object_factory(game_object["res_info"],
                                            game_object["world_position"][0], game_object["world_position"][1])
            elif game_object["type"] == "animation":
                obj = material_animation_object_factory(game_object["res_info"],
                                                        game_object["world_position"][0],
                                                        game_object["world_position"][1])
            else:
                obj = Map(game_object["map_id"], self.director.map_client, self.director.network_client)
            self.map_layer.add_game_object(obj)

        # ShapeLayer
        self.shape_layer = ShapeLayer()

        # UILayer
        self.ui_layer = UILayer()
        for frame in self.scene_init_data["layers"]["ui"]:
            if frame["type"] == "fixed":
                frame_instance = FixedFrame(res_info=frame["res_info"],
                                            x=frame["screen_position"][0], y=frame["screen_position"][1],
                                            w=frame["w"], h=frame["h"])
                for factor in frame["factor"]:
                    if factor["type"] == "button":
                        button_instance = Button(**factor["attributes"])
                        for c in factor["components"]:
                            button_instance.add_component(c)
                        frame_instance.add_child(button_instance)
                    elif factor["type"] == "text_field":
                        text_field_instance = TextField(**factor["attributes"])
                        for c in factor["components"]:
                            text_field_instance.add_component(c)
                        frame_instance.add_child(text_field_instance)
                    elif factor["type"] == "text_input":
                        text_field_instance = TextInput(**factor["attributes"])
                        for c in factor["components"]:
                            text_field_instance.add_component(c)
                        frame_instance.add_child(text_field_instance)
                self.ui_layer.add_game_object(frame_instance)

    def handle_event(self, event):
        if hasattr(self, "on_" + event.name):  # 如果self有该事件的处理方法
            getattr(self, "on_" + event.name)(event)  # 则处理
        if not event.handled:  # 如果该事件没有被handle & obj对象有Children属性
            self.ui_layer.handle_event(event)
        if event.name == "mouse_left_down" and not event.handled:
            self.ui_layer.lose_focus()
        if not event.handled:
            self.shape_layer.handle_event(event)
        if not event.handled:
            self.map_layer.handle_event(event)

    """
    layer 更新流
        event   early   update  late    draw
        
    ui    \      \         /     \        /
    shape  \      \       /       \      /
    map     \      \     /         \    / 
    """
    def update(self, context):
        self.ui_layer.early_update(context)
        self.shape_layer.early_update(context)
        self.map_layer.early_update(context)

        self.map_layer.update(context)
        self.shape_layer.update(context)
        self.ui_layer.update(context)

        self.ui_layer.late_update(context)
        self.shape_layer.late_update(context)
        self.map_layer.late_update(context)

    def draw(self, screen):
        self.map_layer.draw(screen)
        self.shape_layer.draw(screen)
        self.ui_layer.draw(screen)

    def enter(self):
        director.title = self.title
        director.resolution = self.resolution

    def exit(self):
        self.destroy()

    def destroy(self):
        for layer in self.layers:
            layer.destroy()
        del self

    def on_reset_ui_focus(self, event):
        self.ui_layer.lose_focus()
        if hasattr(event, "set_focus_obj"):
            event.set_focus_obj.set_focus()
        event.handled = True
