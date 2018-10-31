import asyncio

from lib.world.director import director
from lib.world.scene import scene_factory

import logging
log = logging.getLogger('')

loop = asyncio.get_event_loop()

scene = director.get_new_scene("newscene/1410.map")

loop.run_until_complete(director.run(loop, scene))
loop.close()
