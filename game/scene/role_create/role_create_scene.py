from core.world.scene import Scene


class RoleCreateScene(Scene):
    scene_init_data = {
        'id': '4',
        'name': 'role_select_scene',
        "title": "大话西游II",
        "resolution": (640, 480),
        "layers": {
            "ui": [
                {
                    "type": "fixed",
                    "screen_position": (0, 0),
                    "w": 640,
                    "h": 480,
                    "res_info": None,
                    "factor": [
                        {
                            "type": "button",
                            "attributes": {
                                "x": 528,
                                "y": 350,
                                "w": 91,
                                "h": 37,
                                "res_info": {"normal": ["gires2.wdf", "0xEA963782"]}
                            },
                            "components": [],
                        },
                        {
                            "type": "button",
                            "attributes": {
                                "x": 528,
                                "y": 410,
                                "w": 91,
                                "h": 37,
                                "res_info": {"normal": ["gires2.wdf", "0xEBD05656"]}
                            },
                            "components": [],
                        }
                    ]
                },
            ],
            "shape": [],
            "map": [
                {
                    "type": "static",
                    "world_position": (0, 0),
                    "res_info": {"normal": ["gires2.wdf", "0x4B291E02"]}
                },
            ]
        }
    }

    def on_mouse_left_down(self, event):
        print(event.pos)
