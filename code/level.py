from game_data import levels
from player import Player
from settings import tile_size, screen_width
from support import import_csv_layout, import_imagedict
from tiles import *


class Level:
    def __init__(self, current_level, surface, create_levelselect, create_level):

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
        self.create_level = create_level
        self.alive = False
        self.counter = 120
        self.starttime = 0

    def setup_level(self, layout):
        tile_img_dict = import_imagedict('../graphics/tile')
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.thorns = pygame.sprite.Group()
        self.checkpoints = pygame.sprite.Group()
        self.enemys = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if cell == '0':
                    tile = Tile((x, y), tile_size, tile_img_dict['ground.png'])
                    self.tiles.add(tile)

                if cell == '4':
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
                    self.checkpoint = (x, y)
                    self.startx = x

                if cell == '6':
                    sprite = Tile((x, y), tile_size, tile_img_dict['spike.png'])
                    self.thorns.add(sprite)

                if cell == '5':
                    sprite = Tile((x, y), tile_size, tile_img_dict['goal.png'])
                    self.goal.add(sprite)

                if cell == '2':
                    sprite = CheckpointTile((x, y), tile_size, tile_img_dict['checkpoint.png'])
                    self.checkpoints.add(sprite)

                if cell == '1':
                    sprite = Enemy((x, y), tile_size, tile_img_dict['enemy'], 10)
                    self.enemys.add(sprite)
                    # TODO 여기 만들기

    def scroll_x(self):
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
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def enemy_horizental_update(self):
        for enemy in self.enemys.sprites():
            enemy.rect.x += enemy.speed.x
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(enemy.rect):
                    if enemy.speed.x < 0:
                        enemy.rect.left = sprite.rect.right
                        enemy.speed.x *= -1
                    elif enemy.speed.x > 0:
                        enemy.rect.right = sprite.rect.left
                        enemy.speed.x *= -1

    def enemy_vertical_update(self):
        for enemy in self.enemys.sprites():
            enemy.apply_gravity()
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(enemy.rect):
                    if enemy.direction.y < 0:
                        enemy.rect.top = sprite.rect.bottom
                        enemy.direction.y = 0

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
            self.time = pygame.time.get_ticks()
            print("level", self.current_level, "time: ", self.time - self.starttime)
            print("time:", self.time)
            print("start_time:",self.starttime)
            levels[self.current_level]['scoreboard'].append(self.time - self.starttime)
            self.create_levelselect(self.new_max_level)

    def check_checkpoint(self):
        checklist = pygame.sprite.spritecollide(self.player.sprite, self.checkpoints, False)
        if checklist:
            self.checkpoint = (checklist[0].pos[0], checklist[0].pos[1])

    def check_thorn(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.thorns, False):
            self.kill_player()

    def check_death(self):
        if self.player.sprite.check_death():
            self.kill_player()

    def kill_player(self):
        self.deathcount += 1
        self.alive = False
        print(self.deathcount)
        self.create_level(self.current_level, self.checkpoint, self.deathcount)

    def startscreen(self):
        if self.counter >= 60:
            self.display_surface.fill('black')
        elif self.counter > 0:
            self.display_surface.fill('grey')
        elif self.counter <= 0:
            self.alive = True
        self.counter -= 3

    def updatetile(self, world_shift):
        self.goal.update(world_shift)
        self.tiles.update(world_shift)
        self.checkpoints.update(world_shift)
        self.thorns.update(world_shift)

    def run(self):
        if self.alive:
            self.scroll_x()
            self.player.sprite.update()
            self.updatetile(self.world_shift)
            self.horizental_movement_collision()

            self.check_checkpoint()
            self.check_thorn()
            self.check_death()
            self.check_win()
            self.vertical_movement_collision()

            self.goal.draw(self.display_surface)
            self.tiles.draw(self.display_surface)
            self.thorns.draw(self.display_surface)
            self.checkpoints.draw(self.display_surface)
            self.player.draw(self.display_surface)
        else:
            self.startscreen()
            self.vertical_movement_collision()
