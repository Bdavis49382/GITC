import json
import pygame
import copy
from constants import TILE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, GRAY,MAP_COLUMNS,MAP_ROWS,GRID_COLUMNS,GRID_ROWS,ENTRANCE

class UI:
    pygame.init()
    def __init__(self,master,client) -> None:
        self._screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption("GITC")
        self.map = []
        self.master = master
        self.client = client
        self.load_file()
    
    def refresh_screen(self,sprites_list):
        self._screen.fill(GRAY)

        self.draw_background()

        sprites_list.update()

        sprites_list.draw(self._screen)

        pygame.display.flip()
        
    def load_file(self):
        self.map = self.client.send('rqst,room')
        self.big_map = self.client.send('rqst,maze')
        # with open('Guide/UI/big_map.json','r') as room_file:
        #     rooms = json.load(room_file)
        #     self.map = rooms['room']
        #     return rooms['maze']



    def draw_background(self):
        tiles = {
            'floor': pygame.image.load('0x72_16x16DungeonTileset.v5/items/floor_plain.png').convert_alpha(),
            'wall': pygame.image.load('0x72_16x16DungeonTileset.v5/items/wall_left.png').convert_alpha()
        }
        for key in tiles:
            tiles[key] = pygame.transform.scale(tiles[key], (TILE_SIZE,TILE_SIZE))
        for big_y in range(GRID_COLUMNS):
            for big_x in range(GRID_ROWS):
                room = self.make_doors(self.big_map[big_y][big_x].split(','))
                for y in range(MAP_ROWS):
                    for x in range(MAP_COLUMNS):
                        self._screen.blit(tiles[room[y][x]],(x*TILE_SIZE+big_x*MAP_COLUMNS*TILE_SIZE,y*TILE_SIZE+big_y*MAP_ROWS*TILE_SIZE))

    def make_doors(self,entrances):
        room = copy.deepcopy(self.map)
        for entrance in entrances:
            x,y = ENTRANCE[entrance]
            room[y][x] = 'floor'
        return room