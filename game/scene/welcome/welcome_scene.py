from core.world.scene import Scene
from core.world.layer import MapLayer
from core.entity.static_object import static_object_factory
from core.entity.material_animation_object import material_animation_object_factory

welcome_scene_json = {
    "id": "1",
    "name": "welcome_scene",
    "title": "大话西游II",
    "resolution": (640, 480),
    "layers": {
        "ui": {

        },
        "shape": None,
        "map": {
            "game_objects": [
                {
                    "type": "static",
                    "world_position": (0, 0),
                    "res_info": {"normal": ["gires2.wdf", "0x5A6AB1AF"]}
                },
                {
                    "type": "material_animation",
                    "world_position": (500, 500),
                    "res_info": {"normal": ["gires2.wdf", "0x23C8D064"]}
                },
            ]
        },
    }

}


class WelcomeScene(Scene):
    def __init__(self, director):
        super().__init__(director)
        self.director.title = welcome_scene_json["title"]
        self.director.resolution = welcome_scene_json["resolution"]

        welcome_map_layer = MapLayer()
        for go in welcome_scene_json["layers"]["map"]["game_objects"]:
            if go["type"] == "static":
                obj = static_object_factory(go["res_info"], go["world_position"][0], go["world_position"][1])
                welcome_map_layer.add_game_object(obj)
            elif go["type"] == "material_animation":
                obj = material_animation_object_factory(go["res_info"], go["world_position"][0], go["world_position"][1])
                welcome_map_layer.add_game_object(obj)
