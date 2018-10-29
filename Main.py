import pygame
from pygame.locals import *

from utils import ptext

from map_client import scene_client, map_connection
from base.events import event_filter

from base.PlayerManager import player_manager as pm
from base.SceneManager import scene_manager as cm
from base.Mouse import get_mouse_point_mask

from game_data import players


def run_game():
    pygame.init()
    pygame.display.set_caption("大话西游Ⅱ")
    screen = pygame.display.set_mode((1100, 600), 0, 32)  # 窗口
    talking_bar = pygame.Surface((300, 600))  # 对话框
    talking_bar.fill((0, 255, 0))
    fps = pygame.time.Clock()

    pm.init_data(players)
    pm.choose_main_player("00001")

    input_data = {
        "scene_client": scene_client,
        "me": pm.me,
        "scene": cm.current,
        "collision_window": Rect(0, 0, 0, 0),
        "window_left_top_pos": (0, 0),
        "ticks": 0,
        "mouse_pos": (0, 0),
        "mouse_mask": None,
        "mask_list": []
    }
    cm.init_scene(scene_client, pm.me.map_name)

    while True:
        fps.tick(40)
        input_data["ticks"] = pygame.time.get_ticks()

        cm.update(input_data)
        pm.update(input_data)

        input_data["mouse_pos"] = pygame.mouse.get_pos()
        input_data["mouse_mask"] = get_mouse_point_mask(input_data["mouse_pos"])
        event_filter(input_data)

        cm.draw()
        pm.draw()

        screen.blit(talking_bar, (800, 0))

        ptext.draw("Target_PC: " + str(pm.me.target), (850, 100), owidth=0.1, ocolor=(0, 0, 0), color=(255, 30, 50))

        ptext.draw("Current_PC: " + str(int(pm.me.current[0])) +", "+ str(int(pm.me.current[1])), (850, 200), owidth=0.5, ocolor=(0, 0, 0), color=(255, 30, 50))

        mouse_pos = pygame.mouse.get_pos()
        ptext.draw("MOUSE: " + str(mouse_pos[0] + input_data["window_left_top_pos"][0]) + "  "
                           + str(mouse_pos[1] + input_data["window_left_top_pos"][1]),
                   (850, 150), owidth=0.5, ocolor=(0, 0, 0), color=(255, 30, 50))

        ptext.draw("MOUSE: " + str(fps), (850, 400), owidth=0.5, ocolor=(0, 0, 0), color=(255, 30, 50))


        pygame.display.flip()

        map_connection.Pump()
        scene_client.Pump()

run_game()