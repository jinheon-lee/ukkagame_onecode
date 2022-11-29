import pygame
import sys
from level import Level
from levelselect import Levelselect
from settings import *


class Game:
    def __init__(self):
        self.current_level = 0
        self.max_level = 0
        self.levelselect = Levelselect(self.max_level, screen, self.create_level)
        self.status = 'levelselect'
        self.deathcount = 0
        self.starttime = 0

    def run(self):
        if self.status == 'levelselect':
            self.levelselect.run()
        else:
            self.level.run()

    def create_level(self, current_level, pos='ukka', deathcount=0):
        self.starttime = self.levelselect.starttime
        self.deathcount = deathcount
        self.status = 'level'
        self.level = Level(current_level, screen, self.create_levelselect, self.create_level)
        if pos != 'ukka':
            self.level.updatetile(-pos[0]+self.level.startx)
            self.level.player.sprite.rect.midleft = (self.level.startx, pos[1])
        self.level.deathcount = self.deathcount

    def create_levelselect(self, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.levelselect = Levelselect(self.max_level, screen, self.create_level)
        self.status = 'levelselect'


# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        game.levelselect.keydown = False
        game.levelselect.mousebuttondown = False
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            game.levelselect.keydown = True
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.levelselect.mousebuttondown = True

    screen.fill('skyblue')
    game.run()

    pygame.display.update()
    clock.tick(60)
