import json
import pygame
import constants
from constants import TILE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, GRAY,MAP_COLUMNS,MAP_ROWS

class UI:
    pygame.init()
    def __init__(self) -> None:
        self._screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption("GITC")
        self.map = []
    
    def refresh_screen(self,sprites_list):
        self._screen.fill(GRAY)

        self.draw_background()

        sprites_list.update()

        sprites_list.draw(self._screen)

        pygame.display.flip()
        
    



    def draw_background(self):
        tiles = {
            'floor': pygame.image.load('0x72_16x16DungeonTileset.v5/items/floor_plain.png').convert_alpha(),
            'wall': pygame.image.load('0x72_16x16DungeonTileset.v5/items/wall_left.png').convert_alpha()
        }
        for key in tiles:
            tiles[key] = pygame.transform.scale(tiles[key], (TILE_SIZE,TILE_SIZE))
        
        for y in range(MAP_ROWS):
            for x in range(MAP_COLUMNS):
                self._screen.blit(tiles[self.map[y][x]],(x*TILE_SIZE,y*TILE_SIZE))