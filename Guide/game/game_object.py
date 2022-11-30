from constants import WHITE,TILE_SIZE,MAP_COLUMNS,MAP_ROWS
import pygame
class Game_object(pygame.sprite.Sprite):

    def __init__(self,maze_pos,pos=0,filename='') -> None:
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

        self.pos = pos

        self.rect.x = maze_pos[0]*TILE_SIZE * MAP_COLUMNS + TILE_SIZE + pos * TILE_SIZE
        self.rect.y = maze_pos[1]*TILE_SIZE * MAP_ROWS + MAP_ROWS * TILE_SIZE//2 

    def update_maze_pos(self,new_maze_pos):
        self.maze_pos = new_maze_pos
        self.rect.x = new_maze_pos[0] * MAP_COLUMNS * TILE_SIZE + TILE_SIZE + self.pos * TILE_SIZE
        self.rect.y = new_maze_pos[1] * MAP_ROWS * TILE_SIZE + MAP_ROWS*TILE_SIZE//2


