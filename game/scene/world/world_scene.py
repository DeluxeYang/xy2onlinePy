from core.world.scene import Scene
from game.character.role import Role


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
            "action": "get_roles",
            "account": self.director.account.account
        })

    def on_receive_roles(self, event):
        if event.account == self.director.account.account:
            for role_data in event.roles:
                role = self.director.account.roles[role_data["role_id"]]
                role.locate(map_id=role_data["map_id"],
                            map_version=role_data["map_version"],
                            x=role_data["x"], y=role_data["y"])
            main_role = self.director.account.get_main_role()
            self.add_map([{
                "type": 'map',
                "map_version": main_role.map_version,
                "map_id": main_role.map_id
            }])
            for role in self.director.account.roles.values():
                self.add_role_to_shape(role)
            self.director.network_client.request(send_data={  # 获取当前地图的portals
                "action": "get_portal_list",
                "map_id": main_role.map_id,
                "map_version": main_role.map_version,
            })
            self.director.network_client.request(send_data={  # 获取当前主要角色所在场景中的其他玩家
                "action": "get_other_players",
                "account": self.director.account.account,
                "map_id": main_role.map_id,
                "map_version": main_role.map_version
            })
            event.handled = True

    def on_receive_other_players(self, event):
        """处理当前场景下其他用户角色"""
        if event.map_id == self.director.account.get_main_role().map_id and \
                event.map_version == self.director.account.get_main_role().map_version:
            for p in event.players:
                role = Role(p['role_id'], p['role_name'],
                            p['level'], p['reborn'],
                            p['race'], p['version'], p['character'], p['gender'])
                role.locate(p['map_id'], p['map_version'], p['x'], p['y'])
                self.add_role_to_shape(role)
            event.handled = True

    def on_receive_portal_list(self, event):
        """处理当前场景下portal"""
        self.add_map(event.portal_list)
        event.handled = True

    def add_role_to_shape(self, role):
        main_role = self.director.account.get_main_role()
        if role.map_id == main_role.map_id and role.map_version == main_role.map_version:
            self.add_shape(role)
