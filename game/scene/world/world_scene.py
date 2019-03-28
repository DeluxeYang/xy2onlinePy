from core.world.scene import Scene


class WorldScene(Scene):
    scene_init_data = {
        "id": "1",
        "name": "world_scene",
        "title": "大话西游II",
        "resolution": (800, 600),
        "layers": {
            "ui": [],
            "shape": [],
            "map": [],
        }
    }

    def network_request(self):
        print(self.director.account.__dict__)
