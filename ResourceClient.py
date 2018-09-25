from __future__ import print_function

from PodSixNet.EndPoint import EndPoint

from Settings import Resource_Port
from base.SceneManager import scene_manager
from base.PlayerManager import player_manager

map_connection = EndPoint()

class MapConnectionListener:
    def Connect(self, *args, **kwargs):
        map_connection.DoConnect(*args, **kwargs)
        # check for connection errors:
        self.Pump()

    def Pump(self):
        for data in map_connection.GetQueue():
            [getattr(self, n)(data) for n in ("Network_" + data['action'], "Network") if hasattr(self, n)]

    def Send(self, data):
        """ Convenience method to allow this listener to appear to send network data, whilst actually using connection. """
        map_connection.Send(data)


class ResourceClient(MapConnectionListener):
    def __new__(cls, host, port):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host, port):
        self.Connect((host, port))

    def get_map_info(self, map_path):
        send_data = {
            'action': "get_map_info",
            'map_file': map_path,
        }
        self.Send(send_data)

    def get_map_unit(self, map_path, unit_num):
        send_data = {
            'action': "get_map_unit",
            'map_file': map_path,
            'unit_num': unit_num
        }
        self.Send(send_data)

    def find_path(self, map_path, current, target, is_running=True):
        send_data = {
            'action': "find_path",
            'map_file': map_path,
            'current': current,
            'target': target,
            'is_running': is_running
        }
        self.Send(send_data)

    def Network(self, data):
        pass
        # print(data.get("error", 0))

    def Network_receive_map_info(self, data):
        scene_manager.current.receive_map(data)

    def Network_receive_map_unit(self, data):
        scene_manager.current.receive_map_unit(data)

    def Network_receive_path_list(self, data):
        player_manager.me.set_target_list(data["path_list"])
        player_manager.me.is_running = data["is_running"]


map_client = ResourceClient( "localhost", int(Resource_Port))