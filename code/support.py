from csv import reader
from os import walk,listdir
import pygame


def import_csv_layout(path):
    terrain_map = []
    with open(path) as mapdata:
        level = reader(mapdata)
        for row in level:
            terrain_map.append(list(row))
        return terrain_map


def import_imagelist(path):
    imglist = []
    for _, __, files in walk(path):
        for image in files:
            if image[-4:] == '.png':
                full_path = path + '/' + image
                image = pygame.image.load(full_path).convert_alpha()
                imglist.append(image)

    return imglist


def import_imagedict(path):
    imgdict = {}
    for image in listdir(path):
        if image[-4:] == '.png':
            full_path = path + '/' + image
            imagefile = pygame.image.load(full_path).convert_alpha()
            imgdict[image] = imagefile
    for __,dirs,_ in walk(path):
        for dir  in dirs:
            full_path = path + '/' + dir
            li = []
            for file in listdir(full_path):
                li.append(file)
            imgdict[dir]=li

    return imgdict