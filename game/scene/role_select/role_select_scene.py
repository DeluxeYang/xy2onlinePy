from core.world.scene import Scene
from core.ui.text_button.text_button import TextButton
from game.scene.role_select.component import \
    CreateButtonComponent, EnterButtonComponent, \
    ExitButtonComponent, RoleNameComponent


class RoleSelectScene(Scene):
    scene_init_data = {
        'id': '4',
        'name': 'role_select_scene',
        "title": "大话西游II",
        "resolution": (640, 480),
        "layers": {
            "ui": [
                {
                    "type": "fixed",
                    "screen_position": (55, 390),
                    "w": 300,
                    "h": 50,
                    "res_info": None,
                    "ui_id": "",
                    "store": {},
                    "factor": [
                        {
                            "type": "button",
                            "attributes": {
                                "x": 0,
                                "y": 0,
                                "w": 91,
                                "h": 37,
                                "res_info": {"normal": ["gires2.wdf", "0xEA963782"]}
                            },
                            "components": [CreateButtonComponent()],
                        },
                        {
                            "type": "button",
                            "attributes": {
                                "x": 91,
                                "y": 0,
                                "w": 91,
                                "h": 37,
                                "res_info": {"normal": ["gires2.wdf", "0xC3E7E556"]}
                            },
                            "components": [EnterButtonComponent()],
                        },
                        {
                            "type": "button",
                            "attributes": {
                                "x": 182,
                                "y": 0,
                                "w": 91,
                                "h": 37,
                                "res_info": {"normal": ["gires2.wdf", "0xEBD05656"]}
                            },
                            "components": [ExitButtonComponent()],
                        }
                    ]
                },
                {
                    "type": "fixed",
                    "screen_position": (90, 70),
                    "w": 200,
                    "h": 280,
                    "res_info": None,
                    "ui_id": "roles_list_frame",
                    "store": {},
                    "factor": [
                        {
                            "type": "fixed",
                            "attributes": {
                                "x": 116,
                                "y": 9,
                                "w": 75,
                                "h": 100,
                                "res_info": None,
                                "ui_id": "avatar"
                            },
                            "components": [],
                        },
                        {
                            "type": "text_field",
                            "attributes": {
                                "text": "",
                                "x": 53,
                                "y": 24,
                                "w": 46,
                                "h": 18,
                                "font_name": "HYC1GJM",
                                "font_size": 16,
                                "sys_font": None,
                                "ui_id": "level"
                            },
                            "components": []
                        },
                        {
                            "type": "text_field",
                            "attributes": {
                                "text": "",
                                "x": 53,
                                "y": 50,
                                "w": 46,
                                "h": 18,
                                "font_name": "HYC1GJM",
                                "font_size": 16,
                                "sys_font": None,
                                "ui_id": "gender"
                            },
                            "components": []
                        },
                        {
                            "type": "text_field",
                            "attributes": {
                                "text": "",
                                "x": 53,
                                "y": 76,
                                "w": 46,
                                "h": 18,
                                "font_name": "HYC1GJM",
                                "font_size": 16,
                                "sys_font": None,
                                "ui_id": "race"
                            },
                            "components": []
                        }
                    ]
                }
            ],
            "shape": [],
            "map": [
                {
                    "type": "static",
                    "world_position": (0, 0),
                    "res_info": {"normal": ["gires2.wdf", "0x66859E78"]}
                },
            ]
        }
    }

    def network_request(self):
        self.director.network_client.request(send_data={
            "action": "get_roles",
            "account": self.director.account.account
        })

    def on_receive_roles(self, event):
        roles_list_frame = self.__getattribute__("roles_list_frame")
        roles_list_frame.store = {}
        y = 128
        for role in event.roles_list:
            roles_list_frame.store[role["role_name"]] = role
            text_button_instance = TextButton(
                text=role["role_name"],
                x=38, y=y,
                w=140, h=18)
            text_button_instance.add_component(RoleNameComponent())
            roles_list_frame.add_child(text_button_instance)
            y += 25
