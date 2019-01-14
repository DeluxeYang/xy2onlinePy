from settings import *

from core.world.director import director

from game.scene.welcome.welcome_scene import WelcomeScene

from game.scene.notice.notice_scene import NoticeScene

from game.scene.world.world_scene import WorldScene

director.run(WelcomeScene)
