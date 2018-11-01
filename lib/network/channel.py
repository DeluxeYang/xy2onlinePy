from __future__ import print_function
import sys
import asynchat


class Channel(asynchat.async_chat):
    end_chars = '\0---\0'

    def __init__(self, conn=None, address=(), server=None, _map=None):
        asynchat.async_chat.__init__(self, getattr(conn, "socket", conn), _map)
        self.address = address
        self._server = server
        self._buffer = b""
        self.set_terminator(self.end_chars.encode())
        self.send_queue = []

    def collect_incoming_data(self, data):
        self._buffer += data

    def found_terminator(self):
        data = self._buffer.decode("utf-8")
        self._buffer = b""
        if isinstance(data, dict) and 'action' in data:
            [getattr(self, n)(data) for n in ('network_' + data['action'], 'network') if hasattr(self, n)]
        else:
            print("Not Json Data: ", data)

    def pump(self):
        [asynchat.async_chat.push(self, d) for d in self.send_queue]
        self.send_queue = []

    def send(self, data):
        """Returns the number of bytes sent after encoding."""
        outgoing = (str(data) + self.end_chars).encode("utf-8")
        self.send_queue.append(outgoing)
        return len(outgoing)

    def handle_connect(self):
        if hasattr(self, "on_connected"):
            self.on_connected()
        else:
            print("Unhandled Connected()")

    def handle_error(self):
        try:
            self.close()
        except Exception as e:
            print(e)
        if hasattr(self, "Error"):
            self.Error(sys.exc_info()[1])
        else:
            asynchat.async_chat.handle_error(self)

    def handle_expt(self):
        pass

    def handle_close(self):
        if hasattr(self, "on_close"):
            self.on_close()
        asynchat.async_chat.handle_close(self)
