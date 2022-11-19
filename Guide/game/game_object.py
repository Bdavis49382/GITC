from constants import WHITE,TILE_SIZE
import pygame
class Game_object(pygame.sprite.Sprite):

    def __init__(self,pos,filename='') -> None:
        super().__init__()
        if filename != '':
            self.image = pygame.image.load(filename).convert_alpha()
            self.rect = self.image.get_rect()
        else:
            self.image = pygame.Surface([TILE_SIZE,TILE_SIZE])
            self.image.fill(WHITE)
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()


        self.tile_pos = pos
        self.rect.x = pos[0]*TILE_SIZE
        self.rect.y = pos[1]*TILE_SIZE

