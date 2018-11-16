from __future__ import print_function

from core.network.end import End
from core.event.event import post_event

from settings import ResourcePort

map_connection = End()

class MapConnectionListener:

    def do_connect(self, *args, **kwargs):
        map_connection.do_connect(*args, **kwargs)
        # check for connection errors:
        self.pump()

    def pump(self):
        for data in map_connection.get_queue():
            [getattr(self, n)(data) for n in ("network_" + data['action'], "network") if hasattr(self, n)]

    @staticmethod
    def transmit(data):
        """
        Convenience method to allow this listener to appear
        to send network data, whilst actually using connection. """
        map_connection.transmit(data)

class MapClient(MapConnectionListener):
    def __new__(cls, host, port):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host, port):
        self.do_connect((host, port))

    def request_map_info(self, map_id):
        send_data = {
            'action': "request_map_info",
            'map_file': map_id,
        }
        self.transmit(send_data)

    def request_map_unit(self, map_id, unit_num):
        send_data = {
            'action': "request_map_unit",
            'map_file': map_id,
            'unit_num': unit_num
        }
        self.transmit(send_data)

    def request_find_path(self, map_id, current, target, is_running=True):
        send_data = {
            'action': "request_find_path",
            'map_file': map_id,
            'current': current,
            'target': target,
            'is_running': is_running
        }
        self.transmit(send_data)

    @staticmethod
    def network(data):
        data["name"] = data["action"]
        post_event(data)

map_client = MapClient( "localhost", int(ResourcePort))
