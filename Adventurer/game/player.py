from game.game_object import Game_object

from constants import TILE_SIZE,ENTRANCE,DEFAULT_POS,TEXTURE_REFERENCE
import pygame

class Player(Game_object):

    def __init__(self,maze_pos,master,pos=DEFAULT_POS) -> None:
        super().__init__(maze_pos,'Player',filename='npc_elf',pos=pos)
        self.master = master
        self.inventory = []
        self.path_taken = [self.maze_pos]
    
    
    def will_collide(self,pos,map):
        if pos[0] < 0:
            self.tile_pos = ENTRANCE['RIGHT']
            self.rect.x = ENTRANCE['RIGHT'][0] * TILE_SIZE
            self.maze_pos[0] -= 1
            self.master.new_room()
            return True
        elif pos[0] >= len(map[0]):
            self.tile_pos = ENTRANCE['LEFT']
            self.rect.x = ENTRANCE['LEFT'][0] * TILE_SIZE
            self.maze_pos[0] += 1
            self.master.new_room()
            return True
        elif pos[1] < 0:
            self.tile_pos = ENTRANCE['BOTTOM']
            self.rect.y = ENTRANCE['BOTTOM'][1] * TILE_SIZE
            self.maze_pos[1] -= 1
            self.master.new_room()
            return True
        elif pos[1] >= len(map):
            self.tile_pos = ENTRANCE['TOP']
            self.rect.y = ENTRANCE['TOP'][1] * TILE_SIZE
            self.maze_pos[1] += 1
            self.master.new_room()
            return True
        elif map[pos[1]][pos[0]] == 'wall':
            return True
        else:
            return False


    def move_right(self,map):
        if not self.will_collide((self.tile_pos[0]+1,self.tile_pos[1]),map):
            self.rect.x += TILE_SIZE
            self.tile_pos = (self.rect.x//TILE_SIZE,self.rect.y//TILE_SIZE)

    def move_left(self,map):
        if not self.will_collide((self.tile_pos[0]-1,self.tile_pos[1]),map):
            self.rect.x -= TILE_SIZE
            self.tile_pos = (self.rect.x//TILE_SIZE,self.rect.y//TILE_SIZE)

    def move_up(self,map):
        if not self.will_collide((self.tile_pos[0],self.tile_pos[1]-1),map):
            self.rect.y -= TILE_SIZE
            self.tile_pos = (self.rect.x//TILE_SIZE,self.rect.y//TILE_SIZE)

    def move_down(self,map):
        if not self.will_collide((self.tile_pos[0],self.tile_pos[1]+1),map):
            self.rect.y += TILE_SIZE
            self.tile_pos = (self.rect.x//TILE_SIZE,self.rect.y//TILE_SIZE)

