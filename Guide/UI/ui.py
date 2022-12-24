import pygame
import copy
from constants import TILE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, GRAY,MAP_COLUMNS,MAP_ROWS,GRID_COLUMNS,GRID_ROWS,ENTRANCE
import sys
sys.path.append('C:/Users/Bdude/OneDrive/Desktop/School Code/GITC\pygame++')
from components.tilemap import Tilemap
from screens.game_screen import Game_screen

class UI:
    pygame.init()
    def __init__(self,master,sprites,client) -> None:
        self._screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption("GITC")
        self.map = []
        self.master = master
        self.client = client
        self.load_files()
        self.background_tile_maps = []
        self.create_background()
        self.game_screen = Game_screen(self._screen,sprites,self.background_tile_maps,[])
        
    def create_background(self):
        for big_y in range(GRID_COLUMNS):
            for big_x in range(GRID_ROWS):
                room = self.make_doors(self.big_maps[self.master.game_level][big_y][big_x].split(','))
                self.background_tile_maps.append(Tilemap(self._screen,room,tile_size=TILE_SIZE,offset=[big_x*TILE_SIZE*MAP_COLUMNS,big_y*TILE_SIZE*MAP_ROWS],size=[MAP_COLUMNS,MAP_ROWS]))

    def load_files(self):
        self.map = self.client.send('rqst,room')
        self.big_maps = self.client.send('rqst,mazes')

    def make_doors(self,entrances):
        room = copy.deepcopy(self.map)
        for entrance in entrances:
            if len(entrance)>1:
                x,y = ENTRANCE[entrance]
                room[y][x] = 'floor'
        return room