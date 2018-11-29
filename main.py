from settings import *

from core.world.director import Director

from game.scene.welcome.welcome_scene import WelcomeScene

director = Director()

scene = WelcomeScene(director=director)

director.run(scene)
