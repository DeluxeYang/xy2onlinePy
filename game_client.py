from res.Characters import characters
from res.MapInfo import map_info

class NetworkClient:
    def __init__(self):
        pass

    def get_scene(self, map_id):
        temp_data = {
            "title": map_info[map_id]["title"],
            "resolution": map_info[map_id]["resolution"],
        }
        return temp_data

    def get_map_portals(self, map_id):
        return map_info[map_id]["portal"]

    def get_players_around(self):
        pass

    def get_player(self, player_id):
        data = {
            "00001": {
                "id": "00001",
                "name": "Deluxe",
                "character": ["mo", "old_1", "nitianmo"],
                "map_id": "newscene/1410.map",
                "position": (500, 500),
            }
        }
        return data[player_id]

    def get_character(self, character_index):
        return characters[character_index[0]][character_index[1]][character_index[2]]


network_client = NetworkClient()
