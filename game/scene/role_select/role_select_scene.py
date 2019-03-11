from core.world.scene import Scene
from game.scene.role_select.component import \
    CreateButtonComponent, EnterButtonComponent, ExitButtonComponent


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
