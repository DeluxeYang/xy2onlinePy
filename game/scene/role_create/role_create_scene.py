from core.world.scene import Scene
from game.scene.role_create.component import CharacterButtonComponent, LeaveButtonComponent, CreateButtonComponent
from res.characters import characters


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
                    "res_info": {"normal": ["gires2.wdf", "0x4B291E02"]},
                    "ui_id": "",
                    "store": {
                        "character_race": "",
                        "character_version": "",
                        "character_name": ""
                    },
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
                            "components": [CreateButtonComponent()],
                        },
                        {
                            "type": "button",  # 离开
                            "attributes": {
                                "x": 528,
                                "y": 410,
                                "w": 91,
                                "h": 37,
                                "res_info": {"normal": ["gires2.wdf", "0xEBD05656"]}
                            },
                            "components": [LeaveButtonComponent()],
                        },
                        {
                            "type": "one_pic_button",  # 俏千金
                            "attributes": {
                                "x": 94,
                                "y": 38,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": characters["ren"]["old"]["qiaoqianjin"]['photo']['m']}
                            },
                            "components": [CharacterButtonComponent(race="ren", version="old", name="qiaoqianjin")],
                        },
                        {
                            "type": "one_pic_button",  # 飞燕女
                            "attributes": {
                                "x": 94,
                                "y": 131,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": characters["ren"]["old"]["feiyannv"]['photo']['m']}
                            },
                            "components": [CharacterButtonComponent(race="ren", version="old", name="feiyannv")],
                        },
                        {
                            "type": "one_pic_button",  # 英女侠
                            "attributes": {
                                "x": 94,
                                "y": 224,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": characters["ren"]["old"]["yingnvxia"]['photo']['m']}
                            },
                            "components": [CharacterButtonComponent(race="ren", version="old", name="yingnvxia")],
                        },
                        {
                            "type": "one_pic_button",  # 逍遥生
                            "attributes": {
                                "x": 20,
                                "y": 38,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": characters["ren"]["old"]["xiaoyaosheng"]['photo']['m']}
                            },
                            "components": [CharacterButtonComponent(race="ren", version="old", name="xiaoyaosheng")],
                        },
                        {
                            "type": "one_pic_button",  # 剑侠客
                            "attributes": {
                                "x": 20,
                                "y": 131,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": characters["ren"]["old"]["jianxiake"]['photo']['m']}
                            },
                            "components": [CharacterButtonComponent(race="ren", version="old", name="jianxiake")],
                        },
                        {
                            "type": "one_pic_button",  # 猛壮士
                            "attributes": {
                                "x": 20,
                                "y": 224,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": characters["ren"]["old"]["mengzhuangshi"]['photo']['m']}
                            },
                            "components": [CharacterButtonComponent(race="ren", version="old", name="mengzhuangshi")],
                        },
                        {
                            "type": "one_pic_button",  # 巨魔王
                            "attributes": {
                                "x": 172,
                                "y": 38,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": characters["mo"]["old"]["jumowang"]['photo']['m']}
                            },
                            "components": [CharacterButtonComponent(race="mo", version="old", name="jumowang")],
                        },
                        {
                            "type": "one_pic_button",  # 夺命妖
                            "attributes": {
                                "x": 172,
                                "y": 131,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": characters["mo"]["old"]["duomingyao"]['photo']['m']}
                            },
                            "components": [CharacterButtonComponent(race="mo", version="old", name="duomingyao")],
                        },
                        {
                            "type": "one_pic_button",  # 虎头怪
                            "attributes": {
                                "x": 172,
                                "y": 224,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": characters["mo"]["old"]["hutouguai"]['photo']['m']}
                            },
                            "components": [CharacterButtonComponent(race="mo", version="old", name="hutouguai")],
                        },
                        {
                            "type": "one_pic_button",  # 狐美人
                            "attributes": {
                                "x": 246,
                                "y": 38,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": characters["mo"]["old"]["humeiren"]['photo']['m']}
                            },
                            "components": [CharacterButtonComponent(race="mo", version="old", name="humeiren")],
                        },
                        {
                            "type": "one_pic_button",  # 小蛮妖
                            "attributes": {
                                "x": 246,
                                "y": 131,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": characters["mo"]["old"]["xiaomanyao"]['photo']['m']}
                            },
                            "components": [CharacterButtonComponent(race="mo", version="old", name="xiaomanyao")],
                        },
                        {
                            "type": "one_pic_button",  # 骨精灵
                            "attributes": {
                                "x": 246,
                                "y": 224,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": characters["mo"]["old"]["gujingling"]['photo']['m']}
                            },
                            "components": [CharacterButtonComponent(race="mo", version="old", name="gujingling")],
                        },
                        {
                            "type": "one_pic_button",  # 神天兵
                            "attributes": {
                                "x": 324,
                                "y": 38,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": characters["xian"]["old"]["shentianbing"]['photo']['m']}
                            },
                            "components": [CharacterButtonComponent(race="xian", version="old", name="shentianbing")],
                        },
                        {
                            "type": "one_pic_button",  # 智圣仙
                            "attributes": {
                                "x": 324,
                                "y": 131,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": characters["xian"]["old"]["zhishengxian"]['photo']['m']}
                            },
                            "components": [CharacterButtonComponent(race="xian", version="old", name="zhishengxian")],
                        },
                        {
                            "type": "one_pic_button",  # 龙战将
                            "attributes": {
                                "x": 324,
                                "y": 224,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": characters["xian"]["old"]["longzhanjiang"]['photo']['m']}
                            },
                            "components": [
                                CharacterButtonComponent(race="xian", version="old", name="longzhanjiang")],
                        },
                        {
                            "type": "one_pic_button",  # 舞天姬
                            "attributes": {
                                "x": 398,
                                "y": 38,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": characters["xian"]["old"]["wutianji"]['photo']['m']}
                            },
                            "components": [CharacterButtonComponent(race="xian", version="old", name="wutianji")],
                        },
                        {
                            "type": "one_pic_button",  # 精灵仙
                            "attributes": {
                                "x": 398,
                                "y": 131,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": characters["xian"]["old"]["jinglingxian"]['photo']['m']}
                            },
                            "components": [CharacterButtonComponent(race="xian", version="old", name="jinglingxian")],
                        },
                        {
                            "type": "one_pic_button",  # 玄剑娥
                            "attributes": {
                                "x": 398,
                                "y": 224,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": characters["xian"]["old"]["xuanjiane"]['photo']['m']}
                            },
                            "components": [CharacterButtonComponent(race="xian", version="old", name="xuanjiane")],
                        },
                        {
                            "type": "animated_frame",
                            "attributes": {
                                "ui_id": "first_weapon",
                                "x": 27,
                                "y": 330,
                                "w": 100,
                                "h": 130,
                                "res_info": None
                            },
                            "components": [],
                        },
                        {
                            "type": "animated_frame",
                            "attributes": {
                                "ui_id": "second_weapon",
                                "x": 140,
                                "y": 330,
                                "w": 100,
                                "h": 130,
                                "res_info": None
                            },
                            "components": [],
                        },
                        {
                            "type": "text_field",
                            "attributes": {
                                "ui_id": "character_introduction",
                                "text": "",
                                "x": 270,
                                "y": 335,
                                "w": 210,
                                "h": 95,
                                "font_name": "HYC1GJM",
                                "font_size": 15
                            },
                            "components": []
                        },
                        {
                            "type": "text_input",
                            "attributes": {
                                "x": 343,
                                "y": 435,
                                "w": 115,
                                "h": 20,
                                "ui_id": "role_name_input"
                            },
                            "components": []
                        },
                    ]
                },
            ],
            "shape": [],
            "map": []
        }
    }

    def on_receive_new_role(self, event):
        from core.event.event import post_event
        from game.scene.role_select.role_select_scene import RoleSelectScene
        post_event({"name": "change_scene", "scene": RoleSelectScene})
        event.handled = True
