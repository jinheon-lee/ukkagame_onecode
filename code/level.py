import sys

import pygame
from tiles import Tile, CheckpointTile
from settings import tile_size, screen_width
from player import Player
from support import import_csv_layout
from game_data import levels


class Level:
    def __init__(self, current_level, surface, create_levelselect):

        # level setup
        self.current_level = current_level
        self.display_surface = surface
        self.level_data = import_csv_layout(levels[current_level]['map'])
        self.setup_level(self.level_data)
        self.world_shift = 0
        self.create_levelselect = create_levelselect
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']
        self.deathcount = 0
        self.checkpoint = (0, 0)

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if cell == '0':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)

                if cell == '4':
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)

                if cell == '5':
                    sprite = Tile((x, y), tile_size, 'yellow')
                    self.goal.add(sprite)

                if cell == '2':
                    checkpoint = CheckpointTile((x, y), tile_size, 'green')
                    self.goal.add(checkpoint)


    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizental_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
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
                    player.on_ceiling = True

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_levelselect(self.new_max_level)

    def check_checkpoint(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.checkpoint):
            pass

    def check_death(self):
        if self.player.sprite.check_death():
            print('사망')
            self.deathcount += 1
            self.goto_checkpoint()
            print(self.deathcount)

    def goto_checkpoint(self):
        pass

    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()
        self.player.update()
        self.horizental_movement_collision()
        self.vertical_movement_collision()
        self.check_death()
        self.check_win()
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
        self.player.draw(self.display_surface)
