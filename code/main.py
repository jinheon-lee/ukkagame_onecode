import pygame
import sys
import csv

import os
import time
import pygame_textinput

level_0 = {
    'map': '../levels/0/level_0_map.csv',
    'pos': (600, 250),
    'selectimgpath': '../graphics/levelselecter/level_0',
    'unlock': 1,
    'scoreboard': [],
    'death': 1000000
}
level_1 = {
    'map': '../levels/1/level_1_map.csv',
    'pos': (600, 350),
    'selectimgpath': '../graphics/levelselecter/level_1',
    'unlock': 2,
    'scoreboard': [],
    'death': 1000000
}
level_2 = {
    'map': '../levels/2/level_2_map.csv',
    'pos': (600, 450),
    'selectimgpath': '../graphics/levelselecter/level_2',
    'unlock': 3,
    'scoreboard': [],
    'death': 1000000
}
level_3 = {
    'map': '../levels/3/level_3_map.csv',
    'pos': (600, 550),
    'selectimgpath': '../graphics/levelselecter/level_3',
    'unlock': 4,
    'scoreboard': [],
    'death': 1000000
}

levels = {
    0: level_0,
    1: level_1,
    2: level_2,
    3: level_3,
}

now_level = 0

class InputBox:
    def __init__(self):
        self.rect = pygame.Rect((100,200),(600,400))
        self.color = 'white'
        self.text = ''
        self.font = pygame.font.Font('../graphics/font/big-shot.ttf', 80)
        print(self.text)
        self.txt_surface = self.font.render(self.text, False, (255,255,255))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(self.text)
                self.text = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = self.font.render(self.text, True, self.color)


    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))


# 텍스트 출력 함수
def text(arg, x, y, arg2=None, fontsize=20, fontcolor=(0, 0, 0), fontname='../graphics/font/neodgm.ttf'):
    font = pygame.font.Font(fontname, fontsize)
    if not arg2:
        text_ = font.render("Score: " + str(int(arg)).zfill(12), True, fontcolor)
    else:
        text_ = font.render(arg2, True, fontcolor)
    textrect = text_.get_rect()
    textrect.centerx = x
    textrect.centery = y
    screen.blit(text_, textrect)


def scoreboard_(now_level):
    screen.fill('black')
    # 스코어보드 입력
    # 1등 기록 금색
    text(0, 640, 100, f"LEVEL {now_level + 1}", 100, (255, 255, 255))
    try:
        text(0, 640, 260, f'1: ' + str(levels[now_level]['scoreboard'][0]).zfill(12), 60, (255, 255, 0))

    except:
        text(0, 640, 260, '1: ' + "0".zfill(12), 60, (255, 255, 0))

    for i in range(1, 9):
        try:
            # 2등 기록 은색
            if i == 1:
                text(0, 400, 260 + (i + 1) // 2 * 80, f'{i + 1}: ' + str(levels[now_level]['scoreboard'][i]).zfill(12),
                     40,
                     (192, 192, 192))
            # 3등 기록 동색
            elif i == 2:
                text(0, 880, 260 + (i + 1) // 2 * 80, f'{i + 1}: ' + str(levels[now_level]['scoreboard'][i]).zfill(12),
                     40,
                     (98, 70, 55))
            # 홀짝성에 따라 좌우 결정
            elif i % 2 == 1:
                text(0, 400, 260 + (i + 1) // 2 * 80, f'{i + 1}: ' + str(levels[now_level]['scoreboard'][i]).zfill(12),
                     40,
                     (255, 255, 255))
            else:
                text(0, 880, 260 + (i + 1) // 2 * 80, f'{i + 1}: ' + str(levels[now_level]['scoreboard'][i]).zfill(12),
                     40,
                     (255, 255, 255))
        except:
            if i == 1:
                text(0, 400, 260 + (i + 1) // 2 * 80, str(i + 1) + ': ' + "0".zfill(12), 40,
                     (192, 192, 192))
            # 3등 기록 동색
            elif i == 2:
                text(0, 880, 260 + (i + 1) // 2 * 80, str(i + 1) + ': ' + "0".zfill(12), 40,
                     (98, 70, 55))
            # 홀짝성에 따라 좌우 결정
            elif i % 2 == 1:
                text(0, 400, 260 + (i + 1) // 2 * 80, str(i + 1) + ': ' + "0".zfill(12), 40,
                     (255, 255, 255))
            else:
                text(0, 880, 260 + (i + 1) // 2 * 80, str(i + 1) + ': ' + "0".zfill(12), 40,
                     (255, 255, 255))
    pygame.display.update()


def import_csv_layout(path):
    terrain_map = []
    with open(path) as mapdata:
        level = csv.reader(mapdata)
        for row in level:
            terrain_map.append(list(row))
        return terrain_map


def import_imagelist(path):
    imglist = []
    for _, __, files in os.walk(path):
        for image in files:
            if image[-4:] == '.png':
                full_path = path + '/' + image
                image = pygame.image.load(full_path).convert_alpha()
                image = pygame.transform.scale(image,(300,90))
                imglist.append(image)

    return imglist


def import_imagedict(path):
    imgdict = {}
    for image in os.listdir(path):
        if image[-4:] == '.png':
            full_path = path + '/' + image
            imagefile = pygame.image.load(full_path).convert_alpha()
            imgdict[image] = imagefile
    for __, dirs, _ in os.walk(path):
        for dir in dirs:
            full_path = path + '/' + dir
            li = []
            for image in os.listdir(full_path):
                if image[-4:] == '.png':
                    full_path = path + '/' + dir + '/' + image
                    imagefile = pygame.image.load(full_path).convert_alpha()
                    li.append(imagefile)
            imgdict[dir] = li

    return imgdict


class Score:
    def __init__(self, name: str, score: int):
        self.name = name
        self.score = score

    def __lt__(self, other):
        self.score < other.score

    def __str__(self):
        return f'{str(self.score).zfill(12)} {self.name}'


def read_scoreboard():
    """레벨의 수만큼 스코어 보드 텍스트 파일을 읽어 game_data.py의 각 레벨의 scoreboard에 저장"""
    for i in range(len(levels)):
        try:
            with open(f'../userscore/scoreboard{i}.txt', 'r') as f:
                lines = f.readlines()
                for j in lines:
                    try:
                        name, score = j.strip().split()
                        levels[i]['scoreboard'].append(Score(name, int(score)))

                    # 스코어보드 파일이 잘못 되었을 경우 초기화
                    except ValueError:
                        levels[i]['scoreboard'] = []
                        break
        # 스코어보드 파일이 존재하지 않을 경우 생성 후 초기화
        except IOError:
            with open(f'../userscore/scoreboard{i}.txt', 'w'):
                pass


class Level:
    def __init__(self, current_level, surface, create_levelselect, create_level):
        # level setup
        self.current_level = current_level  # 현재 레벨
        self.display_surface = surface  # 스크린
        level_data = levels[current_level]  # game_data에서 가져온 레벨의 데이터
        self.map_data = import_csv_layout(level_data['map'])  # 지도(2차원 리스트)
        self.new_unlocked_level = level_data['unlock']  # 이 레벨을 클리어 시 열리는 레벨

        self.create_level = create_level  # 레벨 시작 함수(부활시 사용)
        self.create_levelselect = create_levelselect  # 레벨 선택 시작 함수(승리시 사용)
        self.world_shift = 0  # 플레이어가 고정되어 있고 타일이 움직이게 할 때 사용하는 변수

        self.deathcount = 0  # 죽은 횟수
        self.alive = False  # 부활 화면 실행 여부 판단
        self.counter = 60  # 부활 화면 기능 실행용 카운터
        self.starttime = 0  # 레벨 시작 시간

        self.setup_level(self.map_data)  # 지도 데이터를 이용해 스프라이트들을 생성
        pygame.font.init()
        self.font = pygame.font.Font('../graphics/font/big-shot.ttf', 80)

    def setup_level(self, layout):
        """
        주어진 2차원 맵 데이터를 이용해 스프라이트들의 그룹에 스프라이트를 추가한다

        :param layout:list[list[int]]
        :return:
        """
        self.tile_img_dict = import_imagedict('../graphics/tile')  # 이미지를 dict의 형태로 받아옴
        self.tiles = pygame.sprite.Group()  # 바닥 타일 그룹
        self.player = pygame.sprite.GroupSingle()  # 플레이어 싱글 그룹
        self.goal = pygame.sprite.GroupSingle()  # 골인 지점 싱글 그룹
        self.thorns = pygame.sprite.Group()  # 가시 그룹
        self.checkpoints = pygame.sprite.Group()  # 체크포인트 그룹
        self.enemys = pygame.sprite.Group()  # 적 그룹
        self.mysteryblocks = pygame.sprite.Group()  # 랜덤박스 그룹
        self.detectblocks = pygame.sprite.Group()  # 모서리 표시 블럭 그룹
        # 2차원 리스트를 훑으면서 리스트의 값에 따라 그룹에 해당하는 좌표의 타일 추가하기
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                # 땅
                if cell == '13':
                    tile = Tile((x, y), tile_size, self.tile_img_dict['ground.png'])
                    self.tiles.add(tile)

                # 땅 위의 잔디
                if cell == '16':
                    tile = Tile((x, y), tile_size, self.tile_img_dict['topground.png'])
                    self.tiles.add(tile)

                # 벽돌
                if cell == '21':
                    tile = Tile((x, y), tile_size, self.tile_img_dict['block.png'])
                    self.tiles.add(tile)

                # 플레이어 초기시작 위치
                if cell == '17':
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
                    self.checkpoint = (x, y)
                    self.startx = x

                # 가시
                if cell == '15':
                    sprite = Tile((x, y), tile_size, self.tile_img_dict['spike.png'])
                    self.thorns.add(sprite)

                # 골인점
                if cell == '12':
                    sprite = Tile((x, y), tile_size, self.tile_img_dict['goal.png'])
                    self.goal.add(sprite)

                # 체크포인트
                if cell == '9':
                    sprite = CheckpointTile((x, y), tile_size, self.tile_img_dict['checkpoint.png'])
                    self.checkpoints.add(sprite)

                # 적
                if cell == '20':
                    sprite = Enemy((x, y), tile_size, self.tile_img_dict['enemy'], -2)
                    self.enemys.add(sprite)

                # 랜덤박스
                if cell == '23':
                    sprite = MysteryBlock((x, y), tile_size, self.tile_img_dict['mysteryblock'])
                    self.mysteryblocks.add(sprite)
                # 히든 박스
                if cell == '22':
                    sprite = MysteryBlock((x, y), tile_size, self.tile_img_dict['mysteryblock'], 'hidden')
                    self.mysteryblocks.add(sprite)
                # enemy가 방향 바꾸는 블럭
                if cell == '18':
                    sprite = Detecttile((x, y), tile_size, self.tile_img_dict['enemy_detect.png'])
                    self.detectblocks.add(sprite)

    def scroll_x(self):
        """화면의 위치에 따라  플레이어를 움직일 것인지 화면을 움직일 것인지 결정"""
        playerx = self.player.sprite
        player_x = playerx.rect.centerx
        direction_x = playerx.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            playerx.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            playerx.speed = 0
        else:
            self.world_shift = 0
            playerx.speed = 8

    def horizental_movement_collision(self):
        """플레이어의 좌우이동과 충돌 판정"""
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        # 바닥 타일의 그룹들 과 플레이어의 충돌을 판정하고 위치를 바꾼다
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

        for sprite in self.mysteryblocks.sprites():
            if sprite.status != 'hidden':
                if sprite.rect.colliderect(player.rect):
                    if player.direction.x < 0:
                        player.rect.left = sprite.rect.right
                    elif player.direction.x > 0:
                        player.rect.right = sprite.rect.left

    def enemy_horizental_update(self):
        """enemy의 좌우이동"""
        for enemy in self.enemys.sprites():
            enemy.rect.x += enemy.direction.x

            for sprite in self.detectblocks.sprites():
                if sprite.rect.colliderect(enemy.rect):
                    if enemy.direction.x < 0:
                        enemy.rect.left = sprite.rect.right
                        enemy.direction.x *= -1
                    elif enemy.direction.x > 0:
                        enemy.rect.right = sprite.rect.left
                        enemy.direction.x *= -1

    def enemy_vertical_update(self):
        """enemy의 상하 이동 판정"""
        for enemy in self.enemys.sprites():
            enemy.apply_gravity()
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(enemy.rect):
                    if enemy.direction.y > 0:
                        enemy.rect.bottom = sprite.rect.top
                        enemy.direction.y = 0

    def vertical_movement_collision(self):
        """플레이어의 상하 이동과 충돌 판정"""
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

        # 랜덤 블록(개발중)
        for sprite in self.mysteryblocks.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0 and sprite.status != 'hidden':
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    if sprite.status == 'hidden':
                        player.rect.top = sprite.rect.bottom
                        sprite.status = 'hited'

                    else:
                        player.rect.top = sprite.rect.bottom
                        sprite.status = 'hited'

                    player.direction.y = 0
                    sprite.index = 1

    def check_win(self):
        """골인 지점 도달 체크"""
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.time = pygame.time.get_ticks()
            # print("level", self.current_level, "time: ", self.time - self.starttime)
            # print("time:", self.time)
            # print("start_time:", self.starttime)
            levels[self.current_level]['scoreboard'].append(Score(username, (self.time - self.starttime) // 10))
            if levels[self.current_level]['death'] > self.deathcount:
                levels[self.current_level]['death'] = self.deathcount
                # print(levels[self.current_level]['death'])
            self.create_levelselect(self.new_unlocked_level)

    def check_checkpoint(self):
        """체크리스트 갱신"""
        checklist = pygame.sprite.spritecollide(self.player.sprite, self.checkpoints, False)
        if checklist:
            self.checkpoint = (checklist[0].pos[0], checklist[0].pos[1])

    def check_die(self):
        """가시, 적으로 죽는 것 체크"""
        player = self.player.sprite
        if pygame.sprite.spritecollide(player, self.thorns, False):
            self.kill_player()

        for sprite in pygame.sprite.spritecollide(player, self.enemys, False):
            if abs(sprite.rect.top - player.rect.bottom) < 5:
                sprite.kill()
                player.direction.y = player.jump_speed
            else:
                self.kill_player()

    def check_fall(self):
        """떨어져 죽는 것 체크"""
        if self.player.sprite.check_death():
            self.kill_player()

    def kill_player(self):
        """플레이어 죽이고 레벨 리셋"""
        self.deathcount += 1
        self.alive = False
        # print(self.deathcount)
        self.create_level(self.current_level, self.checkpoint, self.deathcount)  # 체크포인트 이용해 레벨 재생성

    def startscreen(self):
        """부활 시에 보이는 화면"""
        if self.counter >= 0:
            self.display_surface.fill('black')
        elif self.counter <= 0:
            self.alive = True

        text1 = self.font.render(f'x{3 - self.deathcount}', False, 'white')  # 데스카운트 표시
        text2 = self.font.render(f'Level {self.current_level + 1}', False, 'white')  # 레벨 표시
        text2_rect = text2.get_rect(center=(screen_width / 2, screen_height / 2 - 50))  # 텍스트 중앙정렬용 직사각형
        a = self.player.sprite.image.get_rect()  # 플레이어 이미지 가져오기
        a.topright = (screen_width / 2 - 30, screen_height - 285)  # 플레이어 이미지 배치
        self.display_surface.blit(self.player.sprite.image, a)
        self.display_surface.blit(text1, (screen_width / 2 - 10, screen_height - 300))
        self.display_surface.blit(text2, text2_rect)

        self.counter -= 1

    def updatetile(self, world_shift):
        """
        타일 위치 업데이트

        :param world_shift:int
        :return: None
        """
        self.goal.update(world_shift)
        self.tiles.update(world_shift)
        self.checkpoints.update(world_shift)
        self.thorns.update(world_shift)
        self.enemys.update(world_shift)
        self.detectblocks.update(world_shift)
        self.mysteryblocks.update(world_shift)

    def run(self):
        """레벨 실행"""
        if self.alive:
            self.scroll_x()
            self.player.sprite.update()
            self.updatetile(self.world_shift)
            self.horizental_movement_collision()
            self.enemy_horizental_update()
            self.enemy_vertical_update()

            self.check_checkpoint()
            self.check_die()
            self.check_fall()
            self.check_win()
            self.vertical_movement_collision()

            self.goal.draw(self.display_surface)
            self.tiles.draw(self.display_surface)
            self.thorns.draw(self.display_surface)
            self.checkpoints.draw(self.display_surface)
            self.player.draw(self.display_surface)
            self.enemys.draw(self.display_surface)
            self.mysteryblocks.draw(self.display_surface)
        else:
            self.startscreen()
            self.vertical_movement_collision()


class Game:
    """
    전체 게임 클래스
    """

    def __init__(self, current_level):
        self.unlocked_level = 0  # 해금된 레벨(0~self.unlocked_level)
        self.levelselect = Levelselect(self.unlocked_level, screen, self.create_level)  # 레벨 선택 클래스
        self.ending = Ending(screen, self.create_levelselect)  # 엔딩 선택 장면
        self.intro = Intro(screen)  # 인트로
        self.status = 'intro'  # 게임에서 실행중인 것(인트로, 레벨선택, 레벨, 엔딩 등)
        self.deathcount = 0  # 죽은 횟수
        self.starttime = 0  # 레벨 시작
        self.current_level = current_level

    def run(self):
        """
        self.status 따라 장면 실행

        :return: None
        """
        if self.status == 'intro':
            self.intro.run()
            if self.intro.intro_status == 3:
                self.status = 'levelselect'
        elif self.status == 'levelselect':
            self.levelselect.run()
        elif self.status == 'level':
            self.level.run()
        elif self.status == 'ending':
            self.ending.run()
        elif self.status == 'scoreboard':
            scoreboard_(now_level)

    def create_level(self, current_level, pos=None, deathcount=0):
        """
        입력받은 pos 위치에 플레이어가 있는 새 레벨 생성\n
        입력받은 pos 없으면 맵의 기본값으로 설정

        :param current_level: int
        :param pos: tuple
        :param deathcount: int
        :return: None
        """
        self.starttime = self.levelselect.starttime
        self.deathcount = deathcount
        self.status = 'level'
        self.level = Level(current_level, screen, self.create_levelselect, self.create_level)
        if pos is not None:  # pos가 주어졌다면 플레이어의 위치를 새롭게 지정, 체크포인트에 사용
            '''
            여기서 self.level.startx는 레벨에 들어왔을 때 플레이어가 스폰되는 x좌표
            pos를 받은 경우 체크포인트가 보이는 위치의 x좌표가 이 startx가 되게 화면을 이동
            ->pos[0]-self.level.startx만큼 왼쪽으로 world_shift
            그 뒤 화면 기준 startx에에 플레이어 소환
            '''
            self.level.updatetile(-pos[0] + self.level.startx)
            self.level.player.sprite.rect.midleft = (self.level.startx, pos[1])
        self.level.deathcount = self.deathcount

    def create_levelselect(self, new_unlocked_level):
        game.ending.__init__(screen, self.create_levelselect)
        """
        레벨 셀렉트 클래스 만듦

        :param new_unlocked_level: int
        :return:
        """
        # 만약 마지막 스테이지를 깨 new_unlocked_level 인덱스가 레벨의 수와 같으면 엔딩 실행
        if new_unlocked_level == len(levels):
            self.status = 'ending'
            return
        # new_max_level이 기존의 unlocked_level다 작으면 새로운 unlocked_level 업데이트
        if new_unlocked_level > self.unlocked_level:
            self.unlocked_level = new_unlocked_level
        self.levelselect = Levelselect(self.unlocked_level, screen, self.create_level)
        self.status = 'levelselect'


class Intro:
    def __init__(self, display_surface):
        # whitescreen은 게임 화면 규격의 하얀 바탕
        # companylogo는 팀 이름 있는 게임 화면 규격의 이미지
        # logo는 게임 타이틀 있는 게임 화면 규격 이미지
        # 로비는 메뉴 사진

        whitescreenog = pygame.image.load('../graphics/intro/whitescreen.png')
        self.whitescreen = pygame.transform.scale(whitescreenog, (screen_width, screen_height))

        companylogoog = pygame.image.load('../graphics/intro/companylogo.png')
        self.companylogo = pygame.transform.scale(companylogoog, (screen_width, screen_height))

        logoog = pygame.image.load('../graphics/intro/logo.png')
        self.logo = pygame.transform.scale(logoog, (screen_width, screen_height))

        lobbyog = pygame.image.load('../graphics/intro/lobby.png')
        self.lobby = pygame.transform.scale(lobbyog, (screen_width, screen_height))

        self.screen = display_surface
        self.intro_status = 0
        self.screen.fill('white')
        self.timesettrue = 0

    def run(self):
        """인트로 실행"""
        self.playtime = time.time()
        self.whitescreen.set_alpha(40)
        self.screen.fill('white')
        # 처음 시작할 때 로고 나오기, 클릭하면 시작
        if self.timesettrue == 0:
            self.t0 = self.playtime
            self.timesettrue = 1
        if 0 <= self.playtime - self.t0 < 1:
            self.screen.fill('white')

        if 1 <= self.playtime - self.t0 < 2:
            self.screen.fill('white')

        if 2 <= self.playtime - self.t0 < 4:
            self.screen.fill('white')
            self.logo.set_alpha(255 * (self.playtime - self.t0 - 2) / 2)
            self.screen.blit(self.logo, (0, 0))

        if 4 <= self.playtime - self.t0:
            self.screen.blit(self.logo, (0, 0))
            if pygame.mouse.get_pressed()[0]:
                self.timesettrue = 0
                self.intro_status = 1

        if self.intro_status == 1:
            self.screen.fill('black')
            text(0, 390, 120, 'Enter User Name', fontsize=80, fontcolor='white')
            inputbox.draw(self.screen)
            self.t0 = self.playtime

        if self.intro_status == 2 and 0 <= self.playtime - self.t0 < 2:
            self.screen.fill('black')
        if self.intro_status == 2 and 0 <= self.playtime - self.t0 >= 2:
            self.intro_status = 3
        pygame.display.update()


class Ending:
    def __init__(self, display_surface, create_levelselect):
        self.frame = 0

        # 스크린 설정
        self.display_surface = display_surface
        self.display_surface.fill('black')

        # 연출용 플레이어 생성
        self.player = Player((-10, 400))

        # 폰트 설정
        self.font = pygame.font.Font('../graphics/font/neodgm.ttf', 60)
        self.font2 = pygame.font.Font('../graphics/font/neodgm.ttf', 120)
        self.font3 = pygame.font.Font('../graphics/font/neodgm.ttf', 40)

        # 시간계산용 프레임 설정
        self.firstframe = 140
        self.secondframe = 170

        # 엔딩 끝난 후 버튼 설정
        self.button = EndButton((screen_width / 2, 500))

        # 버튼 누를 때 실행하는 함수
        self.create_levelselect = create_levelselect

        self.total_time = 0
        for i in levels.values():
            try:
                self.total_time += min(i['scoreboard']).score
            except:
                pass

        self.total_death = 0
        for i in levels.values():
            self.total_death += i['death']

    def button_check(self):
        """버튼 누르는 것 체크"""
        self.button.text = self.font.render('Return', False, 'white')
        if self.button.rect.collidepoint(pygame.mouse.get_pos()):
            self.button.text = self.font.render('Return', False, 'green')
            if pygame.mouse.get_pressed()[0]:
                self.__init__(self.display_surface, self.create_levelselect)
                self.create_levelselect(len(levels) - 1)
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            self.__init__(self.display_surface, self.create_levelselect)
            self.create_levelselect(len(levels) - 1)

    def run(self):
        """엔딩 실행"""
        self.display_surface.fill('black')
        # 프레임을 기준으로 행동 실행

        # 플레이어 움직임
        if self.frame < 120:
            self.player.rect.x += 5
            self.display_surface.blit(self.player.image, self.player.rect)

        if 120 < self.frame < self.firstframe:
            self.display_surface.blit(self.player.image, self.player.rect)

        # 텍스트 연출
        if self.firstframe <= self.frame < self.firstframe + self.secondframe:
            text1 = '모든 억까를 이겨내고'
            self.key1 = (self.frame - self.firstframe) // 3  # 텍스트 연출 사용 위한 키
            text = self.font.render(text1[:self.key1], False, 'white')
            self.display_surface.blit(text, (100, 200))
            if self.firstframe + 40 <= self.frame:
                text2 = '주인공은 목적지에 도달했다!'
                self.key2 = (self.frame - (self.firstframe + 40)) // 3
                text = self.font.render(text2[:self.key2], False, 'white')
                self.display_surface.blit(text, (100, 300))

        if self.firstframe + self.secondframe < self.frame:
            text = self.font2.render('Game Clear', False, 'white')
            text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2 - 50))
            self.display_surface.blit(text, text_rect)
            if self.firstframe + self.secondframe + 40 < self.frame:
                text1 = 'Thanks for playing'
                self.key1 = (self.frame - (self.firstframe + self.secondframe + 40)) // 3
                text = self.font3.render(text1[:self.key1], False, 'white')
                text_rect = text.get_rect(center=(screen_width / 2, 330))
                self.display_surface.blit(text, text_rect)

        # 돌아가는 버튼 추가
        if self.firstframe + self.secondframe + 150 < self.frame:
            pygame.mouse.set_visible(True)
            self.display_surface.blit(self.button.text, self.button.rect)
            self.button_check()
            text3 = self.font3.render(f'death:{self.total_death}', False, 'white')
            text3_rect = text3.get_rect(midleft=(100, 600))
            self.display_surface.blit(text3, text3_rect)

            text4 = self.font3.render(f'time:{self.total_time}', False, 'white')
            text4_rect = text3.get_rect(midright=(screen_width - 100, 600))
            self.display_surface.blit(text4, text4_rect)

        self.frame += 1


class EndButton(pygame.sprite.Sprite):
    """레벨셀렉트로 돌아가는 버튼"""

    def __init__(self, pos):
        super().__init__()
        self.font = pygame.font.Font('../graphics/font/neodgm.ttf', 60)
        self.text = self.font.render('Return', False, 'white')
        self.rect = self.text.get_rect()
        self.rect.center = pos


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((32, 64))  # 플레이어 이미지
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=pos)  # 플레이어 직사각형
        self.direction = pygame.math.Vector2(0, 0)  # 플레이어 방향벡터(x는 x축 방향설정, y는 y축 속력)
        self.speed = 8  # 플레이어 x방향 속력
        self.gravity = 0.8  # 플레이어에 적용되는 중력
        self.jump_speed = -16  # 플렝이어 점프 시 바뀌는 y방향 속도
        self.on_ground = True  # 땅에 있는지 여부

    def get_input(self):
        """키 입력받아서 방향벡터 수정"""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            self.jump()

    def apply_gravity(self):
        """중력 적용"""
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        self.on_ground = False

    def jump(self):
        """플레이어 점프"""
        if self.on_ground:
            self.direction.y = self.jump_speed
            self.on_ground = False

    def update(self):
        """인풋 받음 """
        self.get_input()

    def check_death(self):
        if self.rect.y > screen_height:
            return True
        else:
            return False


class Levelselect:  # 레벨 선택 클래스
    def __init__(self, unlocked_level, surface, create_level):
        self.lastlevel = len(levels)  # 레벨 수
        self.selected_level = 0  # 선택된 레벨
        self.unlocked_level = unlocked_level  # 해금된 레벨
        self.buttons = pygame.sprite.Group()  # 버튼 클래스 그룹
        self.display_surface = surface  # 스크린
        self.create_level = create_level  # 레벨 생성 함수
        self.starttime = 0  # 게임 시작시부터 시간을 측정하기 위한 변수
        self.cnt = 10  # 키보드 연속입력 제한을 위한 카운터
        self.now_level = now_level

        for i in range(self.lastlevel):
            # 레벨 개수만큼 버튼 만들기
            pos = levels[i]['pos']
            imgpath = levels[i]['selectimgpath']
            img = import_imagelist(imgpath)
            if i <= self.unlocked_level:
                status = 'available'
            else:
                status = 'locked'
            self.buttons.add(LevelselectButton(pos, status, img))

    def displaybutton(self):
        """버튼 상태를 지정하고 버튼 그리기"""
        for i, button in enumerate(self.buttons.sprites()):
            if button.status != 'locked':
                if i == self.selected_level:
                    button.status = 'selected'
                else:
                    button.status = 'unselected'
            else:
                button.status = 'locked'
            button.update()
        self.buttons.draw(self.display_surface)

    def update(self):
        """버튼 누르는 것 확인"""

        global now_level

        # 키보드 입력 확인
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.starttime = pygame.time.get_ticks()
            # print("start:", self.starttime)
            self.create_level(self.selected_level)
            now_level = self.selected_level
            pygame.mouse.set_visible(False)
        elif keys[pygame.K_UP]:
            if self.selected_level >= 1 and self.cnt <= 0:
                self.selected_level -= 1
                self.cnt = 10

        elif keys[pygame.K_DOWN]:
            if self.selected_level < self.unlocked_level and self.cnt <= 0:
                self.selected_level += 1
                self.cnt = 10

        # 마우스 입력 확인
        mousepos = pygame.mouse.get_pos()
        for i, sprite in enumerate(self.buttons.sprites()):
            if sprite.rect.collidepoint(mousepos):
                if i <= self.unlocked_level:
                    self.selected_level = i
                if pygame.mouse.get_pressed()[0] and i <= self.unlocked_level and self.cnt <= 0:
                    self.starttime = pygame.time.get_ticks()
                    now_level = self.selected_level
                    # print("start:", self.starttime)
                    pygame.mouse.set_visible(False)
                    self.create_level(i)
                    self.cnt = 10
        # 연속입력 방지 카운터
        if self.cnt > 0:
            self.cnt -= 1

    def run(self):
        """Levelselect 실행"""
        pygame.mouse.set_visible(True)
        self.update()
        self.displaybutton()
        text(0, screen_width / 2, 110, "UKKA GAME", 120)

    # 아래


class LevelselectButton(pygame.sprite.Sprite):
    def __init__(self, pos, status, imglist):
        super().__init__()
        self.imglist = imglist  # [선택 X 이미지, 선택 이미지, 잠김 이미지]
        self.image = self.imglist[0]  # 선택 안되어있을 때 이미지
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.index = 0
        self.status = status

    def update(self):
        if self.status == 'selected':  # 선택됨
            self.index = 1
        elif self.status == 'unselected':  # 선택 안됨
            self.index = 2
        else:  # 잠김
            self.index = 0

        self.image = self.imglist[self.index]  # 버튼 이미지 업데이트


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        """타일의 위치 업데이트(화면 이동에 쓰임)"""
        self.rect.x += x_shift


class CheckpointTile(Tile):
    def __init__(self, pos, size, img):
        super().__init__(pos, size, img)
        self.pos = self.rect.midleft


class ThornTile(Tile):
    def __init__(self, pos, size, img):
        super().__init__(pos, size, img)


class MultiImageTile(Tile):
    def __init__(self, pos, size, imglist):
        super().__init__(pos, size, imglist[0])
        self.imglist = imglist  # 이미지 리스트로 받음
        self.index = 0

    def update(self, x_shift):
        super().update(x_shift)
        self.image = self.imglist[self.index]


class Enemy(MultiImageTile):
    def __init__(self, pos, size, imglist, speed, gravity=0.8):
        scaledimglist = []
        for image in imglist:
            scaledimglist.append(pygame.transform.scale(image, (48, 48)))
        super().__init__(pos, size, scaledimglist)
        self.direction = pygame.math.Vector2(speed, 0)
        self.gravity = gravity
        self.cnt = 0

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self, x_shift):
        super().update(x_shift)
        self.cnt += 1
        if self.cnt == 20:
            self.cnt = 0
            self.index = 1 - self.index


# 적이 모서리까지 온 것 감지
class Detecttile(Tile):
    def __init__(self, pos, size, img):
        super().__init__(pos, size, img)


class MysteryBlock(MultiImageTile, pygame.sprite.DirtySprite):
    def __init__(self, pos, size, imglist, status='init'):
        super().__init__(pos, size, imglist)
        self.status = status

    def update(self, x_shift):
        if self.status == 'init':
            self.index = 1
            self.visible = 1
        elif self.status == 'hited':
            self.index = 2
            self.visible = 1
        if self.status == 'hidden':
            self.visible = 0

        super().update(x_shift)


# Pygame setup
pygame.init()
pygame.mixer.Sound("../music/AnyConv.com__A.wav").play(-1)
read_scoreboard()
vertical_tile_number = 20
tile_size = 32
screen_height = vertical_tile_number * tile_size
screen_width = 1200
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game(now_level)
pygame.display.set_caption('ukkagame')  # 게임 창 이름
pygame.display.flip()
pygame.key.set_repeat(200, 25)
inputbox = InputBox()

while True:
    events = pygame.event.get()
    for event in events:
        # 게임 닫을 때 세이브데이터 저장하기
        if event.type == pygame.QUIT:
            for ii in range(len(levels)):
                with open(f'../userscore/scoreboard{ii}.txt', 'w') as ff:
                    for jj in sorted(levels[ii]['scoreboard']):
                        ff.write(str(jj) + '\n')
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # esc 누르면 게임 끄기
                if game.status == 'level' or 'ending':  # 레벨이나 엔딩 중이면 레벨 선택하는 곳으로 돌아가기
                    game.ending.__init__(screen, game.create_levelselect)  # Ending 클래스 초기화
                    game.status = 'levelselect'
                else:
                    pygame.quit()
                    sys.exit()
            if event.key == pygame.K_s and game.status == 'levelselect':
                scoreboard_(now_level)
                game.status = 'scoreboard'
            if event.key == pygame.K_e and game.status == 'levelselect' and game.unlocked_level >= len(levels):
                game.status = 'ending'
            if event.key == pygame.K_RETURN and game.intro.intro_status == 1:
                game.intro.intro_status = 2
                username = inputbox.text
        inputbox.handle_event(event)

    screen.fill('skyblue')
    game.run()  # 게임 실행

    pygame.display.update()
    clock.tick(60)
