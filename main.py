import asyncio
import pygame
from pygame import *

from lib.director import director
from lib.scene import scene_factory
from map_client import MapClient

import logging
log = logging.getLogger('')

loop = asyncio.get_event_loop()

scene = scene_factory({"title": "大话西游",
                       "resolution": (800, 600),
                       "fps": 60})

loop.run_until_complete(director.run(loop, scene))
loop.close()
