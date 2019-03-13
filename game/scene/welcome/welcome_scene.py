from core.world.scene import Scene

from .welcome_components import WelcomeEnterButtonMouseComponent, \
    WelcomeExitButtonMouseComponent, WelcomeLinkedButtonMouseComponent


welcome_scene_json = {
    "id": "1",
    "name": "welcome_scene",
    "title": "大话西游II",
    "resolution": (640, 480),
    "layers": {
        "ui": [
            {
                "type": "fixed",
                "screen_position": (460, 80),
                "w": 150,
                "h": 300,
                "res_info": None,
                "ui_id": "",
                "store": {},
                "factor": [
                    {
                        "type": "button",
                        "attributes": {
                            "x": 5,
                            "y": 10,
                            "w": 143,
                            "h": 37,
                            "res_info": {"normal": ["gires2.wdf", "0x0A247197"]}
                        },
                        "components": [WelcomeEnterButtonMouseComponent()],
                    },
                    {
                        "type": "button",
                        "attributes": {
                            "x": 5,
                            "y": 70,
                            "w": 143,
                            "h": 37,
                            "res_info": {"normal": ["gires2.wdf", "0x072DD907"]}
                        },
                        "components": [WelcomeLinkedButtonMouseComponent()],
                    },
                    {
                        "type": "button",
                        "attributes": {
                            "x": 5,
                            "y": 130,
                            "w": 143,
                            "h": 37,
                            "res_info": {"normal": ["gires2.wdf", "0xD139A8FE"]}
                        },
                        "components": [WelcomeExitButtonMouseComponent()],
                    }
                ]
            },
        ],
        "shape": None,
        "map": [
            {
                "type": "static",
                "world_position": (0, 0),
                "res_info": {"normal": ["gires2.wdf", "0x5A6AB1AF"]}
             },
            {
                "type": "animation",
                "world_position": (425, 480-193+113),
                "res_info": {"normal": ["gires2.wdf", "0x23C8D064"]}
            },
            {
                "type": "animation",
                "world_position": (338, 201),
                "res_info": {"normal": ["gires2.wdf", "0xB6C80446"]}
            },
            {
                "type": "static",
                "world_position": (48, 213),
                "res_info": {"normal": ["gires2.wdf", "0xFC849F13"]}
            },
        ]
    }
}


class WelcomeScene(Scene):
    scene_init_data = welcome_scene_json
