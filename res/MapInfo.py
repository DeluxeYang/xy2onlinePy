map_info = {
    "changan_old": {
        "name": "长安城",
        "map_file": "scene/1001.map",
        "portal": [
            {"position": (620, 500), "target_map_id": "huashengsi", "target_position": (3625, 2685), "show": True},
        ],
        "NPC": [
            {"NPC_id": "", "position": (100, 100)},
        ]
    },
    "huashengsi" :{
        "name": "化生寺",
        "map_file" : "scene/1002.map",
        "portal": [
            {"position": (3721, 2754), "target_map_id": "changan", "target_position": (190, 390), "show": True},
        ],
        "NPC": []
    },
    "changan": {
        "name": "长安城",
        "map_file": "newscene/1410.map",
        "portal": [
            {"position": (100, 310), "target_map_id": "huashengsi", "target_position": (3625, 2685), "show": True},
        ],
        "NPC": [
            {"NPC_id": "", "position": (100, 100)},
        ]
    },
}