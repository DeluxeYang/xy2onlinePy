class NetworkClient:
    def __init__(self):
        pass

    def get_scene(self, map_id):
        data = {
            "newscene/1410.map": {
                "title": "大话西游",
                "resolution": (800, 600),
                "portal": [],
                "npc": [],
            }
        }
        return data[map_id]

    def get_players_around(self):
        pass

    def get_player(self, player_id):
        data = {
            "00001": {
                "id": "00001",
                "name": "Deluxe",
                "map_id": "newscene/1410.map",
                "position": (500, 500),
            }

        }
        return data[player_id]


network_client = NetworkClient()
