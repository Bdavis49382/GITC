from constants import TILE_SIZE,DEFAULT_POS
import pygame
import sys
sys.path.append('C:/Users/Bdude/OneDrive/Desktop/School Code/GITC\pygame++')
from node import Node
class Game_object(Node):

    def __init__(self,maze_pos,type,path=[],name='',pos=DEFAULT_POS,filename='') -> None:
        super().__init__(type,name=name,tile_pos=pos,filename=filename)

        self.maze_pos = maze_pos
        self.file_name = filename
        self.path = path
        self.path_pos = 0


