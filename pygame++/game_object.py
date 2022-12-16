from config import WHITE,TILE_SIZE,DEFAULT_POS,TEXTURE_REFERENCE
import pygame
class Game_object(pygame.sprite.Sprite):

    def __init__(self,type,name='',tile_pos=DEFAULT_POS,filename='') -> None:
        super().__init__()
        if filename != '':
            self.image = pygame.image.load(TEXTURE_REFERENCE.format(filename)).convert_alpha()
            self.image = pygame.transform.scale(self.image, (TILE_SIZE,TILE_SIZE))
            self.rect = self.image.get_rect()
        else:
            self.image = pygame.Surface([TILE_SIZE,TILE_SIZE])
            self.image.fill(WHITE)
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()

        self.type = type
        self.name = name
        self.file_name = filename

        self.tile_pos = tile_pos
        self.rect.x = tile_pos[0]*TILE_SIZE
        self.rect.y = tile_pos[1]*TILE_SIZE

