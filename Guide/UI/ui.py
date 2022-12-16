import json
import pygame
import copy
from constants import TILE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, GRAY,MAP_COLUMNS,MAP_ROWS,GRID_COLUMNS,GRID_ROWS,ENTRANCE
import sys
sys.path.append('C:/Users/Bdude/OneDrive/Desktop/School Code/GITC\pygame++')
from tilemap import Tilemap

class UI:
    pygame.init()
    def __init__(self,master,client) -> None:
        self._screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption("GITC")
        self.map = []
        self.master = master
        self.client = client
        self.load_files()
        self.background_tile_maps = []
        self.create_background()
        
    def create_background(self):
        for big_y in range(GRID_COLUMNS):
            self.background_tile_maps.append([])
            for big_x in range(GRID_ROWS):
                room = self.make_doors(self.big_map[big_y][big_x].split(','))
                self.background_tile_maps[big_y].append(Tilemap(self._screen,room,tile_size=TILE_SIZE,offset=[big_x*TILE_SIZE*MAP_COLUMNS,big_y*TILE_SIZE*MAP_ROWS],size=[MAP_COLUMNS,MAP_ROWS]))

    
    def refresh_screen(self,sprites_list):
        self._screen.fill(GRAY)

        self.draw_background()

        sprites_list.update()

        sprites_list.draw(self._screen)

        pygame.display.flip()
        
    def load_files(self):
        self.map = self.client.send('rqst,room')
        self.big_map = self.client.send('rqst,maze')

    def draw_background(self):
        for tilemap_row in self.background_tile_maps:
            for tilemap in tilemap_row:
                tilemap.draw_tiles()

    def make_doors(self,entrances):
        room = copy.deepcopy(self.map)
        for entrance in entrances:
            x,y = ENTRANCE[entrance]
            room[y][x] = 'floor'
        return room