from constants import WHITE,TILE_SIZE,DEFAULT_POS
import pygame
import sys
sys.path.append('C:/Users/Bdude/OneDrive/Desktop/School Code/GITC\pygame++')
from game_object import Game_object
class Game_object(pygame.sprite.Sprite):

    def __init__(self,maze_pos,type,path=[],name='',pos=DEFAULT_POS,filename='') -> None:
        super().__init__()
        if filename != '':
            self.image = pygame.image.load(filename).convert_alpha()
            self.image = pygame.transform.scale(self.image, (TILE_SIZE,TILE_SIZE))
            self.rect = self.image.get_rect()
        else:
            self.image = pygame.Surface([TILE_SIZE,TILE_SIZE])
            self.image.fill(WHITE)
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()

        self.type = type
        self.name = name
        self.maze_pos = maze_pos
        self.file_name = filename
        self.path = path
        self.path_pos = 0

        self.tile_pos = pos
        self.rect.x = pos[0]*TILE_SIZE
        self.rect.y = pos[1]*TILE_SIZE

