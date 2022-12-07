from game.game_object import Game_object
from constants import TILE_SIZE,ENTRANCE,MAP_ROWS,MAP_COLUMNS
import pygame

class Player(Game_object):

    def __init__(self,maze_pos,master,pos=(MAP_COLUMNS//2,MAP_ROWS//2)) -> None:
        super().__init__(maze_pos,'Player')
        self.image = pygame.image.load("0x72_16x16DungeonTileset.v5/items/npc_elf.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE,TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]*TILE_SIZE
        self.rect.y = pos[1]*TILE_SIZE
        self.master = master
        self.maze_pos = maze_pos
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

