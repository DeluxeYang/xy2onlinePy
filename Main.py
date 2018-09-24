import sys
import pygame
from pygame.locals import *

from base.events import event_filter
from base.Mouse import get_mouse_point_mask
from base.interactions.Player import Player
from base.world.SceneManager import scene_manager
from ResourceClient import resource_client, connection
from game_data import main_player, other_players


def run_game():
    pygame.init()
    pygame.display.set_caption("大话西游Ⅱ")
    screen = pygame.display.set_mode((1100, 600), 0, 32)  # 窗口
    talking_bar = pygame.Surface((300, 600))  # 对话框
    talking_bar.fill((0, 255, 0))
    fps = pygame.time.Clock()

    me = Player(main_player)
    scene_manager.init_scene(resource_client, me.map_name)
    scene_manager.current.set_xy(me.current)

    while True:
        fps.tick(40)

        mouse_pos = pygame.mouse.get_pos()
        input_data = {
            "map_client": resource_client,
            "me": me,
            "window_left_top_pos": scene_manager.current.get_left_top(),
            "ticks": pygame.time.get_ticks(),
            "mouse_pos": mouse_pos,
            "mouse_mask": get_mouse_point_mask(mouse_pos),
        }
        event_filter(input_data)

        mask_list = scene_manager.update(input_data)
        input_data["mask_list"] = mask_list

        me.update(input_data)


        screen.blit(talking_bar, (800, 0))
        pygame.display.flip()

        connection.Pump()
        resource_client.Pump()
run_game()