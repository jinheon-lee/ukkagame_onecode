import pygame.font
from settings import *
from game_data import levels
from player import Player


class Ending:
    def __init__(self, display_surface, create_levelselect):
        self.frame = 0
        self.display_surface = display_surface
        self.display_surface.fill('grey')
        self.player = Player((-10, 400))
        self.font = pygame.font.Font('../graphics/font/neodgm.ttf', 60)
        self.font2 = pygame.font.Font('../graphics/font/neodgm.ttf', 120)
        self.font3 = pygame.font.Font('../graphics/font/neodgm.ttf', 40)
        self.firstframe = 140
        self.secondframe = 170
        self.button = EndButton((screen_width / 2, 500))
        self.create_levelselect = create_levelselect

    def button_check(self):
        if self.button.rect.collidepoint(pygame.mouse.get_pos()):
            self.button.text = self.font.render('Return', False, 'green')
            if pygame.mouse.get_pressed()[0]:
                self.create_levelselect(len(levels)-1)
        else:
            self.button.text = self.font.render('Return', False, 'white')

    def run(self):
        self.display_surface.fill('black')
        if self.frame < 120:
            self.player.rect.x += 5
            self.display_surface.blit(self.player.image, self.player.rect)

        if 120 < self.frame < self.firstframe:
            self.display_surface.blit(self.player.image, self.player.rect)
        if self.firstframe <= self.frame < self.firstframe + self.secondframe:
            text1 = '모든 억까를 이겨내고'
            self.key1 = (self.frame - self.firstframe) // 3
            text = self.font.render(text1[:self.key1], False, 'white')
            self.display_surface.blit(text, (100, 200))
            if self.firstframe + 40 <= self.frame:
                text2 = '주인공은 목적지에 도달했다'
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

        if self.firstframe + self.secondframe + 100 < self.frame:
            pygame.mouse.set_visible(True)
            self.display_surface.blit(self.button.text, self.button.rect)
            self.button_check()

        self.frame += 1


class EndButton(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.font = pygame.font.Font('../graphics/font/neodgm.ttf', 60)
        self.text = self.font.render('Return', False, 'white')
        self.rect = self.text.get_rect()
        self.rect.center = pos
