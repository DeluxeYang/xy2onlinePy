from settings import *
from game_client import network_client
from lib.world.director import Director

import logging
log = logging.getLogger('')

director = Director(network_client)

scene = director.get_new_scene("newscene/1410.map")

director.run(scene)
