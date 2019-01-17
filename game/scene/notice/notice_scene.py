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
                        "attributes": {
                            "x": 5,
                            "y": 10,
                            "w": 91,
                            "h": 37,
                            "res_info": {"normal": ["gires2.wdf", "0x703FA361"]}
                        },
                        "components": [NoticeEnterButtonMouseComponent()],
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
                        "type": "text_field",
                        "attributes": {
                            "text": "公告#24#red大话西游#blue大话西游#green大话西游"
                                    "#pink大话西游#yellow大话西游#orange大话西游#brown大话西游#purple大话西游大话西游"
                                    "#sky大话西游大话西游大话西游大话西游大话西游大话西游"
                                    "大话西游大话西游#gold大话西游大话西游大话西游大话西游大话西游#24"
                                    "#tan大话西游大话西游大话西游大话西游大话西游大话西游"
                                    "#grey大话西游大话西游#white大话西游大话西游大话西游大话西游",
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
            {
                "type": "fixed",
                "screen_position": (100, 400),
                "w": 200,
                "h": 50,
                "res_info": None,
                "factor": [
                    {
                        "type": "text_input",
                        "attributes": {
                            "x": 0,
                            "y": 0,
                            "w": 80,
                            "h": 40,
                        },
                        "components": []
                    },
                    {
                        "type": "text_button",
                        "attributes": {
                            "text": "公告#24#red大话西游",
                            "x": 100,
                            "y": 0,
                            "w": 80,
                            "h": 40,
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
