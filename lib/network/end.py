# coding=utf-8
import socket

from asyncore import poll
from .channel import Channel


class End(Channel):
    """
    The endpoint queues up all network events for other classes to read.
    """

    def __init__(self, address=("127.0.0.1", 31425), _map=None):
        self.address = address
        self.is_connected = False
        self.queue = []
        if _map is None:
            self._map = {}
        else:
            self._map = _map
        Channel.__init__(self, _map=self._map)

    def do_connect(self, address=None):
        if address:
            self.address = address
        try:

            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.connect(self.address)
        except socket.gaierror as e:
            self.queue.append({"action": "error", "error": e.args})
        except socket.error as e:
            self.queue.append({"action": "error", "error": e.args})

    def get_queue(self):
        return self.queue

    def pump(self):
        Channel.pump(self)
        self.queue = []
        poll(map=self._map)

    # methods to add network data to the queue depending on network events

    def on_close(self):
        self.is_connected = False
        self.close()
        self.queue.append({"action": "disconnected"})

    def on_connected(self):
        self.queue.append({"action": "socketConnect"})

    def network_connected(self, data):
        self.is_connected = True

    def network(self, data):
        self.queue.append(data)

    def error(self, error):
        self.queue.append({"action": "error", "error": error})

    def connection_error(self):
        self.is_connected = False
        self.queue.append({"action": "error", "error": (-1, "Connection error")})
