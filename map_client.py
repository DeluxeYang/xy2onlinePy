from __future__ import print_function

from lib.network.end import End
from lib.network.connection import ConnectionListener

from settings import ResourcePort

map_connection = End()

class MapClient(ConnectionListener):
    def __new__(cls, host, port):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host, port):
        self.do_connect((host, port))

    def request_map_info(self, map_id):
        send_data = {
            'action': "get_map_info",
            'map_file': map_id,
        }
        self.transmit(send_data)

    def request_map_unit(self, map_id, unit_num):
        send_data = {
            'action': "get_map_unit",
            'map_file': map_id,
            'unit_num': unit_num
        }
        self.transmit(send_data)

    def request_path_finding(self, map_id, current, target, is_running=True):
        send_data = {
            'action': "find_path",
            'map_file': map_id,
            'current': current,
            'target': target,
            'is_running': is_running
        }
        self.transmit(send_data)

    def network(self, data):
        pass

map_client = MapClient( "localhost", int(ResourcePort))
