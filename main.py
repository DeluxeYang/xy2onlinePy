from settings import *

from core.world.director import director

from game.scene.welcome.welcome_scene import WelcomeScene

scene = WelcomeScene()

director.run(scene)
