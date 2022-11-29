import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += x_shift


class CheckpointTile(Tile):
    def __init__(self, pos, size, img):
        super().__init__(pos, size, img)
        self.pos = self.rect.midleft


class ThornTile(Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size, 'blue')
        self.pos = self.rect.cimg


class AnimatedTile(Tile):
    def __init__(self, pos, size, imglist):
        super().__init__(pos, size, imglist[0])
        self.imglist = imglist
        self.index = 0

    def update(self):
        super().update()
        self.image = self.imglist[self.index]


class Enemy(AnimatedTile):
    def __init__(self, pos, size, imglist, speed):
        super().__init__(pos, size, imglist)
        self.speed = pygame.math.Vector2(speed, 0)
        self.gravity = 0.8

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
