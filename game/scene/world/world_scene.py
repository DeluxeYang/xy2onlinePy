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
        self.director.network_client.request(send_data={
            "action": "get_role",
            "account": self.director.account.account,
            "main_role": self.director.account.main_role.name
        })

    def on_receive_role(self, event):
        print(event.__dict__)
        self.add_map([{
            "type": 'map',
            "map_id": event.map_id
        }])
