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


class MultiImageTile(Tile):
    def __init__(self, pos, size, imglist):
        super().__init__(pos, size, imglist[0])
        self.imglist = imglist
        self.index = 0

    def update(self,x_shift):
        super().update(x_shift)
        self.image = self.imglist[self.index]


class Enemy(MultiImageTile):
    def __init__(self, pos, size, imglist, speed, gravity=0):
        super().__init__(pos, size, imglist)
        self.direction = pygame.math.Vector2(speed, 0)
        self.gravity = gravity

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y


class MysteryBlock(MultiImageTile):
    def __init__(self ,pos, size, imglist, hidden=False):
        super().init(pos, size, imglist)



# TODO 지뢰
