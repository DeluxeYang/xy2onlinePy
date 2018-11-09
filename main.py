from settings import *

from core.world.director import Director

import logging
log = logging.getLogger('')

director = Director()

scene = director.get_new_scene("00001", "newscene/1410.map")

director.run(scene)
