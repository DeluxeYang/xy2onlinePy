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
                "ui_id": "",
                "store": {},
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
                "screen_position": (100, 400),
                "w": 200,
                "h": 50,
                "res_info": None,
                "ui_id": "",
                "store": {},
                "factor": [
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

    def network_request(self):
        self.director.network_client.request(send_data={
            "action": "get_announcement"
        })
        from core.event.event import post_event
        post_event({"name": "notify", "text": "大话西游#24大游大话西游大话大话西游大话西游大话西游"})
        post_event({"name": "notify", "text": "大话西游"})

    def on_receive_announcement(self, event):
        self.add_ui([{
            "type": "fixed",
            "screen_position": (100, 100),
            "w": 350,
            "h": 300,
            "res_info": None,
            "ui_id": "",
            "store": {},
            "factor": [
                {
                    "type": "text_field",
                    "attributes": {
                        "text": event.text,
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
        }])
        event.handled = True
