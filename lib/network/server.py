from __future__ import print_function
import socket
import asyncore
from asyncore import poll

from .channel import Channel


class Server(asyncore.dispatcher):
    channel_class = Channel

    def __init__(self, channel_class=None, local_address=("127.0.0.1", 5071), listeners=5):
        if channel_class:
            self.channel_class = channel_class
        self._map = {}
        self.channels = []
        asyncore.dispatcher.__init__(self, map=self._map)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)  # socket
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.set_reuse_addr()
        self.bind(local_address)  # bind
        self.listen(listeners)

    def handle_accept(self):
        try:
            conn, address = self.accept()
        except socket.error:
            print('warning: server accept() threw an exception')
            return
        except TypeError:
            print('warning: server accept() threw EWOULDBLOCK')
            return
        self.channels.append(self.channel_class(conn, address, self, self._map))
        self.channels[-1].send({"action": "connected"})
        if hasattr(self, "on_connected"):
            self.on_connected(self.channels[-1], address)

    def pump(self):
        [c.pump() for c in self.channels]
        poll(map=self._map)
