from core.world.scene import Scene
from core.world.layer import MapLayer, UILayer
from core.entity.static_object import static_object_factory
from core.entity.material_animation_object import material_animation_object_factory

from core.ui.frame.frame import FixedFrame
from core.ui.button.button import Button


welcome_scene_json = {
    "id": "1",
    "name": "welcome_scene",
    "title": "大话西游II",
    "resolution": (640, 480),
    "layers": {
        "ui": [
            {
                "type": "fixed",
                "screen_position": (100, 100),
                "w": 100,
                "h": 100,
                "res_info": None,
                "factor": [
                    {
                        "type": "button",
                        "relative_position": (100, 100),
                        "w": 100,
                        "h": 100,
                        "components": None,
                        "res_info": {"normal": ["gires2.wdf", "0xC3E7E556"]}
                    }
                ]
            }
        ],
        "shape": None,
        "map": [
            {
                "type": "static",
                "world_position": (0, 0),
                "res_info": {"normal": ["gires2.wdf", "0x5A6AB1AF"]}
             },
            {
                "type": "material_animation",
                "world_position": (425, 480-193+113),
                "res_info": {"normal": ["gires2.wdf", "0x23C8D064"]}
            },
            {
                "type": "material_animation",
                "world_position": (338, 201),
                "res_info": {"normal": ["gires2.wdf", "0xB6C80446"]}
            },
            {
                "type": "static",
                "world_position": (48, 213),
                "res_info": {"normal": ["gires2.wdf", "0xFC849F13"]}
            },
        ]
    }
}


class WelcomeScene(Scene):
    def __init__(self, director):
        super().__init__(director)
        self.title = welcome_scene_json["title"]
        self.resolution = welcome_scene_json["resolution"]

        welcome_map_layer = MapLayer()
        for game_object in welcome_scene_json["layers"]["map"]:
            if game_object["type"] == "static":
                obj = static_object_factory(game_object["res_info"],
                                            game_object["world_position"][0], game_object["world_position"][1])
                welcome_map_layer.add_game_object(obj)
            elif game_object["type"] == "material_animation":
                obj = material_animation_object_factory(game_object["res_info"],
                                                        game_object["world_position"][0], game_object["world_position"][1])
                welcome_map_layer.add_game_object(obj)

        ui_layer = UILayer()
        for frame in welcome_scene_json["layers"]["ui"]:
            if frame["type"] == "fixed":
                frame_instance = FixedFrame(res_info=frame["res_info"],
                                            x=frame["screen_position"][0], y=frame["screen_position"][0],
                                            w=frame["w"], h=frame["h"])
                for factor in frame["factor"]:
                    if factor["type"] == "button":
                        button_instance = Button(res_info=factor["res_info"],
                                            x=factor["relative_position"][0], y=factor["relative_position"][0],
                                            w=factor["w"], h=factor["h"])
                        frame_instance.add_child(button_instance)
                ui_layer.add_game_object(frame_instance)

        self.add_layer(ui_layer)
        self.add_layer(welcome_map_layer)