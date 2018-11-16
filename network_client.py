from __future__ import print_function

from core.network.end import End
from core.event.event import post_event

from settings import NetworkPort

network_connection = End()

class NetworkConnectionListener:

    def do_connect(self, *args, **kwargs):
        network_connection.do_connect(*args, **kwargs)
        # check for connection errors:
        self.pump()

    def pump(self):
        for data in network_connection.get_queue():
            [getattr(self, n)(data) for n in ("network_" + data['action'], "network") if hasattr(self, n)]

    @staticmethod
    def transmit(data):
        """
        Convenience method to allow this listener to appear
        to send network data, whilst actually using connection. """
        network_connection.transmit(data)

class NetworkClient(NetworkConnectionListener):
    def __new__(cls, host, port):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host, port):
        self.do_connect((host, port))

    def request(self, send_data):
        self.transmit(send_data)

    @staticmethod
    def network(data):
        data["name"] = data["action"]
        post_event(data)

network_client = NetworkClient( "localhost", int(NetworkPort))
