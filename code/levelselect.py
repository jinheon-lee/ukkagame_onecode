import pygame

from game_data import levels
from support import import_imagelist


class Levelselect:

    def __init__(self, maxlevel, surface, create_level):
        self.lastlevel = len(levels)
        self.selected_level = 0
        self.maxlevel = maxlevel
        self.buttons = pygame.sprite.Group()
        self.display_surface = surface
        self.keydown = False
        self.create_level = create_level
        self.mousebuttondown = False
        self.starttime = 0

        for i in range(self.lastlevel):
            pos = levels[i]['pos']
            imgpath = levels[i]['selectimgpath']
            img = import_imagelist(imgpath)
            if i <= self.maxlevel:
                status = 'available'
            else:
                status = 'locked'
            self.buttons.add(Button(pos, status, img))

    def displaybutton(self):
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
        if self.keydown:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                self.starttime = pygame.time.get_ticks()
                print("start:", self.starttime)
                self.create_level(self.selected_level)
            elif keys[pygame.K_UP]:
                if self.selected_level >= 1:
                    self.selected_level -= 1
                    pygame.time.delay(300)
            elif keys[pygame.K_DOWN]:
                if self.selected_level < self.maxlevel:
                    self.selected_level += 1
                    pygame.time.delay(300)

        mousepos = pygame.mouse.get_pos()
        for i, sprite in enumerate(self.buttons.sprites()):
            if sprite.rect.collidepoint(mousepos):
                self.selected_level = i
        if self.mousebuttondown:
            self.starttime = pygame.time.get_ticks()
            print("start:", self.starttime)
            self.create_level(self.selected_level)

    def run(self):
        self.displaybutton()
        self.update()

    # 아래


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, status, img):
        super().__init__()
        self.imglist = img
        self.image = self.imglist[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.index = 0
        self.status = status

    def update(self):
        if self.status == 'selected':
            self.index = 1
        elif self.status == 'unselected':
            self.index = 2
        else:
            self.index = 0

        self.image = self.imglist[self.index]
