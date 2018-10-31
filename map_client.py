import asyncio
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

    async def connect(self, loop):
        self.loop = loop
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port, loop=self.loop)
        self.loop.create_task(self._handle_packets())
        self.loop.create_task(self._send())

    async def _handle_packets(self):
        while self.running:
            data = await self.reader.readuntil(b"}")
            if not data:
                continue
            message = data.decode()
            print(message)
            log.debug("(NET) Received " + message)

    def send(self, send_data):
        data = str(send_data).encode()
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
