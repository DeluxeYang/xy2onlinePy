from PodSixNet.Connection import connection
from PodSixNet.Connection import ConnectionListener

from base.world.SceneManager import scene_manager
from Settings import Resource_Port


class ResourceClient(ConnectionListener):
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

    def Network(self, data):
        pass
        # print(data.get("error", 0))

    def Network_receive_map_info(self, data):
        scene_manager.current.receive_map(data)

    def Network_receive_map_unit(self, data):
        scene_manager.current.receive_map_unit(data)


resource_client = ResourceClient( "localhost", int(Resource_Port))
