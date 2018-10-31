import asyncio

from settings import *
from map_client import MapClient
from game_client import NetworkClient
from lib.world.director import Director

import logging
log = logging.getLogger('')

loop = asyncio.get_event_loop()

map_client = MapClient("localhost", ResourcePort)

network_client = NetworkClient()

director = Director(map_client, network_client, loop)

scene = director.get_new_scene("newscene/1410.map")

director.start(scene)

loop.create_task(map_client.connect(loop))

loop.run_forever()

loop.close()
