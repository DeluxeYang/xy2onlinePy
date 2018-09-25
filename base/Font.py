import pygame
from utils.Math import get_window_pc

pygame.font.init()
font = pygame.font.SysFont('fangsong', 17, bold=True)  # 通过字体文件获得字体对象


def render_text(content, color=(0, 0, 0)):
    text = font.render(content, True, color)
    text_shadow = font.render(content, True, (0,0,0))
    return text, text_shadow


def blit_text(text, text_shadow, left_top, world_pc, desc=0):
    screen = pygame.display.get_surface()
    window_pc = get_window_pc(left_top, world_pc)
    text_rect = text.get_rect()
    text_shadow_rect = text_shadow.get_rect()
    text_rect.center = (window_pc[0], window_pc[1] + desc)

    text_shadow_rect.center = (window_pc[0]+1, window_pc[1]+desc)
    screen.blit(text_shadow, text_shadow_rect)  # 绘制字体


    screen.blit(text, text_rect)  # 绘制字体