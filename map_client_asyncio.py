import asyncio

from lib.event.event import post_event
import logging
log = logging.getLogger('')


class MapClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.loop = None
        self.running = True
        self.reader = None
        self.writer = None
        self.send_q = asyncio.Queue()

        self.read_task = None
        self.send_task = None

    async def connect(self, loop):
        self.loop = loop
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port,
                                                                 loop=self.loop, limit=2**32)
        self.read_task = asyncio.create_task(self._handle_packets())
        self.send_task = asyncio.create_task(self._send())

    async def _handle_packets(self):
        while self.running:
            data = await self.reader.readline()
            message = data.decode()

            response = eval(message)
            if response["name"] == "receive_map_info":
                post_event(response)
            elif response["name"] == "receive_map_unit":
                post_event(response)
            elif response["name"] == "receive_path_list":
                post_event(response)

    def send(self, send_data):
        data = str(send_data).encode() + b"\n"
        self.send_q.put_nowait(data)

    async def _send(self):
        while self.running:
            data = await self.send_q.get()
            self.writer.write(data)
            await self.writer.drain()

    def disconnect(self):
        print("MapClient Disconnect")
        self.running = False
        self.writer.close()
        self.read_task.cancel()
        self.send_task.cancel()
