import sys

import pygame

from game_data import levels
from level import Level
from levelselect import Levelselect
from settings import *

def read_scoreboard():
    for i in range(len(levels)):
        try:
            with open(f'../userscore/scoreboard{i}.txt', 'r') as f:
                lines = f.readlines()
                for j in lines:
                    try:
                        score = j.strip()
                        levels[i]['scoreboard'].append(score)

                    # 스코어보드 파일이 잘못 되었을 경우 초기화
                    except ValueError as err:
                        levels[i]['scoreboard'] = {}
                        break
        # 스코어보드 파일이 존재하지 않을 경우 생성 후 초기화
        except IOError:
            with open(f'../userscore/scoreboard{i}.txt', 'w') as f:
                pass


class Game:
    def __init__(self):
        self.current_level = 0
        self.max_level = 2
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
            self.level.updatetile(-pos[0] + self.level.startx)
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
read_scoreboard()

while True:
    for event in pygame.event.get():
        game.levelselect.keydown = False
        game.levelselect.mousebuttondown = False
        if event.type == pygame.QUIT:
            for i in range(len(levels)):
                with open(f'../userscore/scoreboard{i}.txt', 'w') as ff:
                    for j in levels[i]['scoreboard']:
                        ff.write(str(j) + '\n')
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
