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
            data = await self.reader.read()
            if not data:
                continue
            message = data.decode()
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


'''
import asyncio
import pygame
import logging
from pygame import *
log = logging.getLogger('')



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