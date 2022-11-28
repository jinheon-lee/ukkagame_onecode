from csv import reader
from os import walk
import pygame


def import_csv_layout(path):
    terrain_map = []
    with open(path) as mapdata:
        level = reader(mapdata)
        for row in level:
            terrain_map.append(list(row))
        return terrain_map


def import_image_forder(path):
    imglist = []
    for _, __, files in walk(path):
        for image in files:
            if image[-4:] == '.png':
                full_path = path + '/' + image
                image = pygame.image.load(full_path).convert_alpha()
                imglist.append(image)

    return imglist
