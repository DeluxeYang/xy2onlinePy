from core.world.scene import Scene
from game.scene.role_create.component import CharacterButtonComponent


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
                        },
                        {
                            "type": "one_pic_button",  # 俏千金
                            "attributes": {
                                "x": 94,
                                "y": 38,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": ["photo.wdf", "0x7C5EC587"]}
                            },
                            "components": [CharacterButtonComponent(race="ren", version="old_0", name="qiaoqianjin")],
                        },
                        {
                            "type": "one_pic_button",  # 飞燕女
                            "attributes": {
                                "x": 94,
                                "y": 131,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": ["photo.wdf", "0xE230B836"]}
                            },
                            "components": [CharacterButtonComponent(race="ren", version="old_0", name="feiyannv")],
                        }
                        ,
                        {
                            "type": "one_pic_button",  # 英女侠
                            "attributes": {
                                "x": 94,
                                "y": 224,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": ["photo.wdf", "0xDDB93FB2"]}
                            },
                            "components": [CharacterButtonComponent(race="ren", version="old_0", name="yingnvxia")],
                        },
                        {
                            "type": "one_pic_button",  # 逍遥生
                            "attributes": {
                                "x": 20,
                                "y": 38,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": ["photo.wdf", "0xA171FA71"]}
                            },
                            "components": [CharacterButtonComponent(race="ren", version="old_0", name="xiaoyaosheng")],
                        },
                        {
                            "type": "one_pic_button",  # 剑侠客
                            "attributes": {
                                "x": 20,
                                "y": 131,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": ["photo.wdf", "0x23F50F01"]}
                            },
                            "components": [CharacterButtonComponent(race="ren", version="old_0", name="jianxiake")],
                        },
                        {
                            "type": "one_pic_button",  # 猛壮士
                            "attributes": {
                                "x": 20,
                                "y": 224,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": ["photo.wdf", "0x397FDA0C"]}
                            },
                            "components": [CharacterButtonComponent(race="ren", version="old_0", name="mengzhuangshi")],
                        },
                        {
                            "type": "one_pic_button",  # 巨魔王
                            "attributes": {
                                "x": 172,
                                "y": 38,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": ["photo.wdf", "0x6C5D9B16"]}
                            },
                            "components": [CharacterButtonComponent(race="mo", version="old_0", name="jumowang")],
                        },
                        {
                            "type": "one_pic_button",  # 夺命妖
                            "attributes": {
                                "x": 172,
                                "y": 131,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": ["photo.wdf", "0xF446FF01"]}
                            },
                            "components": [CharacterButtonComponent(race="mo", version="old_0", name="duomingyao")],
                        }
                        ,
                        {
                            "type": "one_pic_button",  # 虎头怪
                            "attributes": {
                                "x": 172,
                                "y": 224,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": ["photo.wdf", "0x5C6DCFF7"]}
                            },
                            "components": [CharacterButtonComponent(race="mo", version="old_0", name="hutouguai")],
                        },
                        {
                            "type": "one_pic_button",  # 狐美人
                            "attributes": {
                                "x": 246,
                                "y": 38,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": ["photo.wdf", "0x4C6D73C9"]}
                            },
                            "components": [CharacterButtonComponent(race="mo", version="old_0", name="humeiren")],
                        },
                        {
                            "type": "one_pic_button",  # 小蛮妖
                            "attributes": {
                                "x": 246,
                                "y": 131,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": ["photo.wdf", "0x5AE145E5"]}
                            },
                            "components": [CharacterButtonComponent(race="mo", version="old_0", name="xiaomanyao")],
                        },
                        {
                            "type": "one_pic_button",  # 骨精灵
                            "attributes": {
                                "x": 246,
                                "y": 224,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": ["photo.wdf", "0x5763727F"]}
                            },
                            "components": [CharacterButtonComponent(race="mo", version="old_0", name="gujingling")],
                        },
                        {
                            "type": "one_pic_button",  # 神天兵
                            "attributes": {
                                "x": 324,
                                "y": 38,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": ["photo.wdf", "0xC842C91B"]}
                            },
                            "components": [CharacterButtonComponent(race="xian", version="old_0", name="shentianbing")],
                        },
                        {
                            "type": "one_pic_button",  # 智圣仙
                            "attributes": {
                                "x": 324,
                                "y": 131,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": ["photo.wdf", "0x7B27BA25"]}
                            },
                            "components": [CharacterButtonComponent(race="xian", version="old_0", name="zhishengxian")],
                        }
                        ,
                        {
                            "type": "one_pic_button",  # 龙战将
                            "attributes": {
                                "x": 324,
                                "y": 224,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": ["photo.wdf", "0x09193986"]}
                            },
                            "components": [CharacterButtonComponent(race="xian", version="old_0", name="longzhanjiang")],
                        },
                        {
                            "type": "one_pic_button",  # 舞天姬
                            "attributes": {
                                "x": 398,
                                "y": 38,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": ["photo.wdf", "0xEE9E4601"]}
                            },
                            "components": [CharacterButtonComponent(race="xian", version="old_0", name="wutianji")],
                        },
                        {
                            "type": "one_pic_button",  # 精灵仙
                            "attributes": {
                                "x": 398,
                                "y": 131,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": ["photo.wdf", "0x2381820C"]}
                            },
                            "components": [CharacterButtonComponent(race="xian", version="old_0", name="jinglingxian")],
                        },
                        {
                            "type": "one_pic_button",  # 玄剑娥
                            "attributes": {
                                "x": 398,
                                "y": 224,
                                "w": 65,
                                "h": 85,
                                "res_info": {"normal": ["photo.wdf", "0xB301105E"]}
                            },
                            "components": [CharacterButtonComponent(race="xian", version="old_0", name="xuanjiane")],
                        }
                    ]
                },
            ],
            "shape": [],
            "map": []
        }
    }

    def on_mouse_left_down(self, event):
        print(event.pos)
