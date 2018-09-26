import pygame
from pygame.locals import *

from ResourceClient import scene_client, map_connection
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

        font = pygame.font.SysFont(None, 24)  # 通过字体文件获得字体对象
        text = font.render("Target_PC: " + str(pm.me.target), True, (0, 0, 0))  # 配置要显示的文字
        text_rect = text.get_rect()  # 获得要显示的对象的rect
        text_rect.center = (900, 150)  # 设置显示对象的坐标
        screen.blit(text, text_rect)  #

        text = font.render("Current_PC: " + str(pm.me.current), True, (0, 0, 0))  # 配置要显示的文字
        text_rect = text.get_rect()  # 获得要显示的对象的rect
        text_rect.center = (900, 200)  # 设置显示对象的坐标
        screen.blit(text, text_rect)  # 绘制字体

        mouse_pos = pygame.mouse.get_pos()
        text = font.render("MOUSE: " + str(mouse_pos[0] + input_data["window_left_top_pos"][0]) + "  "
                           + str(mouse_pos[1] + input_data["window_left_top_pos"][1]), True,
                           (0, 0, 0))  # 配置要显示的文字
        text_rect = text.get_rect()  # 获得要显示的对象的rect
        text_rect.center = (900, 300)  # 设置显示对象的坐标
        screen.blit(text, text_rect)  # 绘制字体
        pygame.display.update()

        text = font.render("MOUSE: " + str(fps), True, (0, 0, 0))  # 配置要显示的文字
        text_rect = text.get_rect()  # 获得要显示的对象的rect
        text_rect.center = (900, 400)  # 设置显示对象的坐标
        screen.blit(text, text_rect)  # 绘制字体
        pygame.display.flip()



        pygame.display.flip()

        map_connection.Pump()
        scene_client.Pump()

run_game()