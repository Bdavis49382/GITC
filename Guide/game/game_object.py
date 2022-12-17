from constants import WHITE,TILE_SIZE,MAP_COLUMNS,MAP_ROWS
import pygame
import sys
sys.path.append('C:/Users/Bdude/OneDrive/Desktop/School Code/GITC\pygame++')
from node import Node
class Game_object(Node):

    def __init__(self,type,maze_pos,pos=0,filename='') -> None:

        super().__init__(type,tile_pos = [maze_pos[0] * MAP_COLUMNS + pos + 1,maze_pos[1] * MAP_ROWS + MAP_ROWS//2],filename=filename,tile_size=TILE_SIZE)

        self.pos = pos # position in the room. Either 0, 1, or 2

    def update_maze_pos(self,new_maze_pos):
        self.maze_pos = new_maze_pos
        self.rect.x = new_maze_pos[0] * MAP_COLUMNS * TILE_SIZE + TILE_SIZE + self.pos * TILE_SIZE
        self.rect.y = new_maze_pos[1] * MAP_ROWS * TILE_SIZE + MAP_ROWS*TILE_SIZE//2


