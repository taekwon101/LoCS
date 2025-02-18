import pygame
from ztile import *
from zplayer import Player
from zsettings import *

class Level:
    def __init__(self):

       #get the display surface
       self.display_surface = pygame.display.get_surface()
       
       # sprite group setup
       self.visible_sprites = YSortCameraGroup()
       self.obstacle_sprites = pygame.sprite.Group()

       #sprite setup
       self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                
                #display environment objects
                if col == 'x':
                    Tree((x,y),[self.visible_sprites, self.obstacle_sprites])
                if col == 'r1':
                    Rock1((x,y),[self.visible_sprites, self.obstacle_sprites])
                #display player model
                if col == 'p':
                    self.player = Player((x,y),[self.visible_sprites], self.obstacle_sprites, pygame.key.get_pressed)

    def run(self):
        #update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):

        #getting the offset 
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)