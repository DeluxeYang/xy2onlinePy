map_info = {
    "scene/1001.map": {
        "title": "大话西游",
        "resolution": (800, 600),
        "name": "长安城",
        "portal": [
            {"position": (620, 500), "target_map_id": "scene/1002.map", "target_position": (3625, 2685),
             "show": True, "wdf": "mapani.wdf", "hash": "0xC0570C07"},
        ],
        "NPC": [
            {"NPC_id": "", "position": (100, 100)},
        ]
    },
    "scene/1002.map": {
        "title": "大话西游",
        "resolution": (800, 600),
        "name": "化生寺",
        "portal": [
            {"position": (3721, 2754), "target_map_id": "newscene/1410.map", "target_position": (190, 390),
             "show": True, "wdf": "mapani.wdf", "_hash": "0xC0570C07"},
        ],
        "NPC": []
    },
    "newscene/1410.map": {
        "title": "大话西游",
        "resolution": (800, 600),
        "name": "长安城",
        "portal": [
            {"position": (100, 310), "target_map_id": "scene/1002.map", "target_position": (3625, 2685),
             "show": True, "wdf": "mapani.wdf", "_hash": "0xC0570C07"},
        ],
        "NPC": {}
    },
}