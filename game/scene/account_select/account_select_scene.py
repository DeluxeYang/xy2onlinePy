from core.world.scene import Scene
from game.scene.account_select.component import \
    EnterButtonMouseComponent, CancelButtonMouseComponent


class AccountSelectScene(Scene):
    scene_init_data = {
        "id": "3",
        "name": "account_select_scene",
        "title": "大话西游II",
        "resolution": (640, 480),
        "layers": {
            "ui": [
                {
                    "type": "fixed",
                    "screen_position": (270, 180),
                    "w": 250,
                    "h": 110,
                    "res_info": None,
                    "factor": [
                        {
                            "type": "text_input",
                            "attributes": {
                                "x": 0,
                                "y": 5,
                                "w": 240,
                                "h": 20,
                                "input_id": "username_input"
                            },
                            "components": []
                        },
                        {
                            "type": "button",
                            "attributes": {
                                "x": 40,
                                "y": 70,
                                "w": 91,
                                "h": 37,
                                "res_info": {"normal": ["gires2.wdf", "0xC3E7E556"]}
                            },
                            "components": [EnterButtonMouseComponent()],
                        },
                        {
                            "type": "button",
                            "attributes": {
                                "x": 160,
                                "y": 70,
                                "w": 91,
                                "h": 37,
                                "res_info": {"normal": ["gires2.wdf", "0xCB250B45"]}
                            },
                            "components": [CancelButtonMouseComponent()],
                        },
                    ]
                },
            ],
            "shape": [

            ],
            "map": [
                {
                    "type": "static",
                    "world_position": (0, 0),
                    "res_info": {"normal": ["gires2.wdf", "0x51F941C4"]}
                },
            ]
        }
    }
