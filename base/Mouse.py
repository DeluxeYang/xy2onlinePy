import pygame
from pygame.locals import Rect

from utils.Mask import Mask

mouse_mask = pygame.Mask((2, 2))
mouse_mask.fill()

def get_mouse_point_mask(mouse_pos):
    mouse_rect = Rect(mouse_pos[0], mouse_pos[1], 2, 2)
    return Mask(mouse_rect, mouse_mask)