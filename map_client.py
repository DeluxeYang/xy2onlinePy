import asyncio

from settings import ResourcePort


class MapClient:
    def __new__(cls, host, port):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host, port):
        self.reader = None
        self.writer = None
        self.host = host
        self.port = port

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)

    def send(self, send_data):
        data = str(send_data).encode()
        self.writer.write(data)

    def close(self):
        self.writer.close()

    async def get_map_info(self, map_id):
        send_data = {
            'request': "map_info",
            'map_id': map_id,
        }
        self.send(send_data)
        return await self.read()

    async def get_map_unit(self, map_id, unit_num):
        send_data = {
            'request': "map_unit",
            'map_id': map_id,
            'unit_num': unit_num
        }
        self.send(send_data)
        return await self.read()

    async def find_path(self, map_id, current, target, is_running=True):
        send_data = {
            'request': "find_path",
            'map_id': map_id,
            'current': current,
            'target': target,
            'is_running': is_running
        }
        self.send(send_data)
        return await self.read()

    async def read(self):
        data = await self.reader.read()
        return data


'''
import asyncio
import pygame
import logging
from pygame import *
log = logging.getLogger('')


class Client:
    def __init__(self, host, port, loop):
        self.host = host
        self.port = port
        self.loop = loop
        self.send_q = asyncio.Queue()

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, 
                                                                 self.port, 
                                                                 loop=self.loop)
        self.loop.create_task(self._handle_packets())
        self.loop.create_task(self._send())

    async def _handle_packets(self):
        while True:
            data = await self.reader.read(4096)
            if not data:
                continue
            message = data.decode()
            log.debug("(NET) Received "+message)

    def send(self, data):
        self.send_q.put_nowait(data)

    async def _send(self):
        while True:
            data = await self.send_q.get()
            self.writer.write(data)
            await self.writer.drain()

    def disconnect(self):
        print("DC")
        self.writer.close()


async def main(loop):
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Pyond client")
    bg = Surface((640, 480))
    bg.fill(Color("#004400"))
    client = Client('127.0.0.1', 2508, loop)
    await client.connect()
    while True:
        pygame.event.pump()
        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit
            elif e.type == KEYUP:
                if e.key == K_UP:
                    client.send(b"{'Hello':'World'}")
        screen.blit(bg, (0, 0))
        pygame.display.update()
    client.disconnect()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
'''