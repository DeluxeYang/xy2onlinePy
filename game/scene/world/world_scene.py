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
        self.director.network_client.request(send_data={  # 首先获取main_role的数据
            "action": "get_role",
            "account": self.director.account.account,
            "role": self.director.account.get_main_role().name,  # 获取main_role的数据
            "is_main_role": True
        })

    def on_receive_main_role(self, event):
        self.specify_role(event, is_main_role=True)  # 载入role数据
        self.director.account.set_main_role(event.role_name)
        self.add_map([{
            "type": 'map',
            "map_id": event.map_id
        }])
        for role_name in self.director.account.roles:  # 再获取其他角色数据
            if self.director.account.get_main_role().name != role_name:
                self.director.network_client.request(send_data={
                    "action": "get_role",
                    "account": self.director.account.account,
                    "role": role_name,
                    "is_main_role": False
                })

    def on_receive_role(self, event):
        self.specify_role(event, is_main_role=False)
        event.handled = True

    def specify_role(self, data, is_main_role):
        role = self.director.account.roles[data.role_name]
        role.specify(
            level=data.role_level, reborn=data.role_reborn,
            race=data.race, version=data.version, character=data.character,
            map_id=data.map_id, x=data.x, y=data.y
        )
        self.add_role_to_shape(role, is_main_role)  # 加入到shape层

    def add_role_to_shape(self, role, is_main_role):
        if is_main_role:
            self.add_shape(role)
        else:
            if role.map_id == self.director.account.get_main_role().map_id:
                self.add_shape(role)
