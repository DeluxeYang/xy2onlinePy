from core.world.director import director
from core.world.layer import MapLayer, UILayer, ShapeLayer

from core.entity.static_object import static_object_factory
from core.entity.material_animation_object import material_animation_object_factory

from core.ui.frame.frame import FixedFrame, AnimatedFrame
from core.ui.button.button import Button
from core.ui.one_pic_button.button import OnePicButton
from core.ui.text_field.text_field import TextField
from core.ui.text_input.text_input import TextInput
from core.ui.text_button.text_button import TextButton
from core.ui.notify.notify import Notify

from game.map.map import Map


class Scene:
    scene_init_data = None

    def network_request(self):
        pass

    def __init__(self):
        self.director = director
        self.ui_layer = None
        self.shape_layer = None
        self.map_layer = None
        self.network_request()

        self.title = self.scene_init_data["title"]
        self.resolution = self.scene_init_data["resolution"]
        # MapLayer
        self.map_layer = MapLayer()
        self.add_map(self.scene_init_data["layers"]["map"])
        # ShapeLayer
        self.shape_layer = ShapeLayer()
        self.add_shape(self.scene_init_data["layers"]["shape"])
        # UILayer
        self.ui_layer = UILayer()
        self.add_ui(self.scene_init_data["layers"]["ui"])

        self.notify_x = 260 if self.resolution[0] == 800 else 180
        self.notify_y = 220 if self.resolution[1] == 600 else 170

        self.notify_count = 0
        self.notify_max = 15
        self.notify_frame = FixedFrame(res_info=None,
                                       x=self.notify_x, y=self.notify_y,
                                       w=400, h=300)
        self.ui_layer.add_game_object(self.notify_frame)

    def add_map(self, map_object_list):
        for game_object in map_object_list:
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

    def reset_map_layer(self):
        self.map_layer.destroy()
        self.map_layer = MapLayer()

    def add_shape(self, shape):
        self.shape_layer.add_game_object(shape)

    def reset_shape_layer(self):
        self.shape_layer.destroy()
        self.shape_layer = ShapeLayer()

    def add_ui(self, ui_object_list):
        for frame in ui_object_list:
            if frame["type"] == "fixed":
                frame_instance = FixedFrame(res_info=frame["res_info"],
                                            x=frame["screen_position"][0], y=frame["screen_position"][1],
                                            w=frame["w"], h=frame["h"], ui_id=frame["ui_id"], store=frame["store"])
                if frame_instance.ui_id != "":
                    self.__setattr__(frame_instance.ui_id, frame_instance)
                for factor in frame["factor"]:
                    if factor["type"] == "button":
                        button_instance = Button(**factor["attributes"])
                        for c in factor["components"]:
                            button_instance.add_component(c)
                        frame_instance.add_child(button_instance)
                    if factor["type"] == "one_pic_button":
                        button_instance = OnePicButton(**factor["attributes"])
                        for c in factor["components"]:
                            button_instance.add_component(c)
                        frame_instance.add_child(button_instance)
                    elif factor["type"] == "text_field":
                        text_field_instance = TextField(**factor["attributes"])
                        for c in factor["components"]:
                            text_field_instance.add_component(c)
                        frame_instance.add_child(text_field_instance)
                    elif factor["type"] == "text_input":
                        text_input_instance = TextInput(**factor["attributes"])
                        for c in factor["components"]:
                            text_input_instance.add_component(c)
                        frame_instance.add_child(text_input_instance)
                    elif factor["type"] == "text_button":
                        text_button_instance = TextButton(**factor["attributes"])
                        for c in factor["components"]:
                            text_button_instance.add_component(c)
                        frame_instance.add_child(text_button_instance)
                    elif factor["type"] == "notify":
                        notify_instance = Notify(**factor["attributes"])
                        for c in factor["components"]:
                            notify_instance.add_component(c)
                        frame_instance.add_child(notify_instance)
                    elif factor["type"] == "animated_frame":
                        _instance = AnimatedFrame(**factor["attributes"])
                        for c in factor["components"]:
                            _instance.add_component(c)
                        frame_instance.add_child(_instance)
                    elif factor["type"] == "fixed":
                        _instance = FixedFrame(**factor["attributes"])
                        for c in factor["components"]:
                            _instance.add_component(c)
                        frame_instance.add_child(_instance)
                if frame_instance.ui_id != "":
                    self.__setattr__(frame_instance.ui_id, frame_instance)
                self.ui_layer.add_game_object(frame_instance)

    def reset_ui_layer(self):
        self.ui_layer.destroy()
        self.ui_layer = UILayer()

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
        self.map_layer.destroy()
        self.map_layer = None
        self.shape_layer.destroy()
        self.shape_layer = None
        self.ui_layer.destroy()
        self.ui_layer = None
        self.director = None
        del self

    def on_reset_ui_focus(self, event):
        self.ui_layer.lose_focus()
        if hasattr(event, "set_focus_obj"):
            event.set_focus_obj.set_focus()
        event.handled = True

    def on_notify(self, event):
        self.notify_count = min(len(self.notify_frame.children), 10)
        self.notify_count = self.notify_count % self.notify_max
        notify_instance = Notify(
            res_info={"normal": ["gires.wdf", "0x8D580095"]},
            x=10*self.notify_count, y=10*self.notify_count,
            text=event.text
        )
        self.notify_frame.add_child(notify_instance)
        self.notify_count += 1
        event.handled = True
