from game.game_object import Game_object
from constants import TILE_SIZE,MAP_ROWS,MAP_COLUMNS
import pygame

class Player(Game_object):

    def __init__(self, maze_pos,master) -> None:
        super().__init__(maze_pos)
        self.image = pygame.image.load("0x72_16x16DungeonTileset.v5/items/npc_elf.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE,TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = maze_pos[0]*TILE_SIZE * MAP_COLUMNS + MAP_COLUMNS * TILE_SIZE//2
        self.rect.y = maze_pos[1]*TILE_SIZE * MAP_ROWS + MAP_ROWS * TILE_SIZE//2

        self.master = master
        self.maze_pos = [ 0, 0 ]
    

