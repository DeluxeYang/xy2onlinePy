import pygame

from ResourceClient import map_client, map_connection
from base.events import event_filter

from base.PlayerManager import player_manager as pm
from base.SceneManager import scene_manager as sm
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

    sm.init_scene(map_client, pm.me.map_name)
    sm.current.set_xy(pm.me.current)

    while True:
        fps.tick(40)

        mouse_pos = pygame.mouse.get_pos()
        left_top = sm.current.get_left_top()
        input_data = {
            "map_client": map_client,
            "me": pm.me,
            "scene": sm.current,
            "window_left_top_pos": left_top,
            "ticks": pygame.time.get_ticks(),
            "mouse_pos": mouse_pos,
            "mouse_mask": get_mouse_point_mask(mouse_pos),
        }
        event_filter(input_data)

        sm.current.set_xy(pm.me.current)
        mask_list = sm.update(input_data)
        input_data["mask_list"] = mask_list

        pm.update(input_data)





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
        text = font.render("MOUSE: " + str(mouse_pos[0] + left_top[0]) + "  " + str(mouse_pos[1] + left_top[1]), True,
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
        map_client.Pump()
run_game()