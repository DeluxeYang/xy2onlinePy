import gc
import pygame
from pygame.locals import *
from utils.res_manager import res_manager

pygame.init()

pygame.display.set_mode((800, 600))

directory = 'shape.wdf'

wdf = res_manager.get_wdf(directory)

for _hash in list(wdf.file_dict.keys())[696:]:
    was = res_manager.get_res(directory, _hash)
    if not was:
        continue
    i = 0
    j = 0
    h = len(was.image_group)
    w = len(was.image_group[0])
    size = was.image_group[0][0].get_size()
    image = pygame.Surface((size[0] * w, size[1] * h), pygame.SRCALPHA)

    for images in was.image_group:
        j = 0
        for im in images:
            position = (size[0] * j, size[1] * i)  # was关键点 - 帧图片关键点
            image.blit(im, position)
            j += 1
        i += 1

    pygame.image.save(image, directory + '/' + _hash + '_' + str(h) + '_' + str(w) + '.png')
    gc.collect()

