from __future__ import print_function

from lib.network.end import End

map_connection = End()

class MapConnectionListener:
    def connect(self, *args, **kwargs):
        map_connection.do_connect(*args, **kwargs)
        # check for connection errors:
        self.pump()

    def pump(self):
        for data in map_connection.get_queue():
            [getattr(self, n)(data) for n in ("Network_" + data['action'], "Network") if hasattr(self, n)]

    def send(self, data):
        """ Convenience method to allow this listener to appear to send network data, whilst actually using connection. """
        map_connection.send(data)

class ResourceClient(MapConnectionListener):
    def __new__(cls, host, port):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host, port):
        self.connect((host, port))

    def get_map_info(self, map_path):
        send_data = {
            'action': "get_map_info",
            'map_file': map_path,
        }
        self.send(send_data)


scene_client = ResourceClient("localhost", 9999)

while 1:
    map_connection.pump()
    scene_client.pump()