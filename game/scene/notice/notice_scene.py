from core.world.scene import Scene
from .notice_components import NoticeEnterButtonMouseComponent


notice_scene_json = {
    "id": "1",
    "name": "welcome_scene",
    "title": "大话西游II",
    "resolution": (640, 480),
    "layers": {
        "ui": [
            {
                "type": "fixed",
                "screen_position": (530, 378),
                "w": 100,
                "h": 50,
                "res_info": None,
                "factor": [
                    {
                        "type": "button",
                        "relative_position": (5, 10),
                        "w": 91,
                        "h": 37,
                        "components": [NoticeEnterButtonMouseComponent()],
                        "res_info": {"normal": ["gires2.wdf", "0x703FA361"]}
                    },
                ]
            },
            {
                "type": "fixed",
                "screen_position": (100, 100),
                "w": 350,
                "h": 300,
                "res_info": None,
                "factor": [
                    {
                        "type": "textfield",
                        "attributes": {
                            "text": "公告#24大话西游大话西游大话西游大话西游大话西游大话西游大话西游#24"
                                    "大话西游大话西游大话西游大话西游大话西游大话西游"
                                    "大话西游大话西游大话西游大话西游大话西游大话西游"
                                    "大话西游大话西游大话西游大话西游大话西游大话西游大话西游#24"
                                    "大话西游大话西游大话西游大话西游大话西游大话西游"
                                    "大话西游大话西游大话西游大话西游大话西游大话西游",
                            "res_info": None,
                            "x": 0,
                            "y": 0,
                            "w": 350,
                            "h": 300,
                            "font_name": None,
                            "font_size": 16,
                            "sys_font": "simsunnsimsun"
                        },
                        "components": []
                    },
                ]
            },
        ],
        "shape": None,
        "map": [
            {
                "type": "static",
                "world_position": (0, 0),
                "res_info": {"normal": ["gires2.wdf", "0x27689D65"]}
             },
            {
                "type": "static",
                "world_position": (0, 0),
                "res_info": {"normal": ["gires2.wdf", "0xE8FD733B"]}
             }
        ]
    }
}


class NoticeScene(Scene):
    scene_init_data = notice_scene_json
