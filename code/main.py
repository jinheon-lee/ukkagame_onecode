import sys

import pygame

from game_data import levels
from level import Level
from levelselect import Levelselect
from settings import *
import time
from ending import Ending

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
        # self.max_level = 2
        self.max_level = 0
        self.levelselect = Levelselect(self.max_level, screen, self.create_level)
        self.status = 'levelselect'
        # self.status = 'ending'
        self.deathcount = 0
        self.starttime = 0
        self.ending = Ending(screen,self.create_levelselect)


    def run(self):
        if self.status == 'levelselect':
            self.levelselect.run()
        elif self.status == 'level':
            self.level.run()
        elif self.status == 'ending':
            self.ending.run()

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
        if new_max_level == len(levels):
            self.status = 'ending'
            return
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.levelselect = Levelselect(self.max_level, screen, self.create_level)
        self.status = 'levelselect'
        pygame.mouse.set_visible(True)


# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()
read_scoreboard()

# screen는 디스플레이고, 아마 니네 코드에서는 screen 이런걸로 돼있을 가능성 큼. 정의는 다음과 같이 나감
# screen이라 돼있으면 screen --> screen으로 다 바꿔

timesettrue = 0
screen.fill((0, 0, 0))
pygame.display.set_caption('')
pygame.display.flip()

white = (255, 255, 255)

# whitescreen은 게임 화면 규격의 하얀 바탕
# companylogo는 니네 팀 이름 있는 게임 화면 규격의 이미지
# logo는 게임 타이틀 있는 게임 화면 규격 이미지
# 로비는 메뉴 사진

whitescreenog = pygame.image.load('../graphics/intro/whitescreen.png')
whitescreen = pygame.transform.scale(whitescreenog, (screen_width, screen_height))

companylogoog = pygame.image.load('../graphics/intro/companylogo.png')
companylogo = pygame.transform.scale(companylogoog, (screen_width, screen_height))

logoog = pygame.image.load('../graphics/intro/logo.png')
logo = pygame.transform.scale(logoog, (screen_width, screen_height))

lobbyog = pygame.image.load('../graphics/intro/lobby.png')
lobby = pygame.transform.scale(lobbyog, (screen_width, screen_height))

gamemode = 'opening'

intro_over = False

while not intro_over:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()

    playtime = time.time()
    whitescreen.set_alpha(40)

    # 처음 시작할 때 로고 나오기, 클릭하면 로비로 가기
    if gamemode == 'opening':
        if timesettrue == 0:
            t0 = playtime
            timesettrue = 1
        if 0 <= playtime - t0 < 1:
            screen.blit(whitescreen, (0, 0))
        if 3 <= playtime - t0 < 5:
            screen.fill(white)
            companylogo.set_alpha(255 * (playtime - t0 - 3) / 2)
            screen.blit(companylogo, (0, 0))
        if 7 <= playtime - t0 < 9:
            screen.fill(white)
            companylogo.set_alpha(255 * (9 - playtime + t0) / 2)
            screen.blit(companylogo, (0, 0))

        if 10 <= playtime - t0 < 11:
            screen.fill(white)

        if 11 <= playtime - t0 < 13:
            screen.fill(white)
            logo.set_alpha(255 * (playtime - t0 - 11) / 2)
            screen.blit(logo, (0, 0))

        if 13 <= playtime - t0:
            if event.type == pygame.MOUSEBUTTONDOWN:
                timesettrue = 0
                intro_over = True

    pygame.display.update()
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
