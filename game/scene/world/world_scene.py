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
            "action": "get_role",
            "account": self.director.account.account,
            "role": self.director.account.get_main_role().name,  # 获取main_role的数据
            "is_main_role": True
        })

    def on_receive_main_role(self, event):  # 获取到主要角色信息
        """获取到主要角色信息"""
        self.specify_role(event, is_main_role=True)  # 载入role数据
        self.director.account.set_main_role(event.role_name)
        self.add_map([{
            "type": 'map',
            "map_version": event.map_version,
            "map_id": event.map_id
        }])
        """request当前地图的portals"""
        self.director.network_client.request(send_data={  # 获取当前地图的portals
            "action": "get_portal_list",
            "map_id": event.map_id,
            "map_version": event.map_version,
        })
        """request当前账号其他角色数据"""
        for role_name in self.director.account.roles:  # 再获取当前账号其他角色数据
            if self.director.account.get_main_role().name != role_name:
                self.director.network_client.request(send_data={
                    "action": "get_role",
                    "account": self.director.account.account,
                    "role": role_name,
                    "is_main_role": False
                })
        """request当前主要角色所在场景中的其他玩家"""
        self.director.network_client.request(send_data={  # 获取当前主要角色所在场景中的其他玩家
            "action": "get_other_players",
            "account": self.director.account.account,
            "map_id": self.director.account.get_main_role().map_id,
            "map_version": self.director.account.get_main_role().map_version
        })
        event.handled = True

    def on_receive_role(self, event):
        """处理当前用户角色"""
        self.specify_role(event, is_main_role=False)
        event.handled = True

    def on_receive_other_players(self, event):
        """处理当前场景下其他用户角色"""
        if event.map_id == self.director.account.get_main_role().map_id and \
                event.map_version == self.director.account.get_main_role().map_version:
            for p in event.players:
                role = Role(p['role_name'], p['level'], p['reborn'],
                            p['race'], p['version'], p['character'], p['gender'])
                role.specify(p['map_id'], p['map_version'], p['x'], p['y'])
                self.add_role_to_shape(role)
            event.handled = True

    def on_receive_portal_list(self, event):
        """处理当前场景下portal"""
        self.add_shape(event.portal_list)
        event.handled = True

    def specify_role(self, data, is_main_role):
        role = self.director.account.roles[data.role_name]
        role.specify(map_id=data.map_id, map_version=data.map_version, x=data.x, y=data.y)
        self.add_role_to_shape(role, is_main_role)  # 加入到shape层

    def add_role_to_shape(self, role, is_main_role=False):
        if is_main_role:
            self.add_shape(role)
            role.init()
        else:
            if role.map_id == self.director.account.get_main_role().map_id and \
                    role.map_version == self.director.account.get_main_role().map_version:
                self.add_shape(role)
                role.init()
