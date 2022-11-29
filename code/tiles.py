import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, color='grey'):
        # TODO 색깔이 아니라 이미지로 하기
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += x_shift


class CheckpointTile(Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size, 'green')
        self.pos = self.rect.center


class ThornTile(Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size, 'blue')
        self.pos = self.rect.center

class AnimatedTile(Tile):
    def __init__(self):
        super.__init__()
        pass