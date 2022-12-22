import pygame
from constants import TILE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, GRAY,MAP_COLUMNS,MAP_ROWS,WHITE,BLACK,RED
import sys
sys.path.append('C:/Users/Bdude/OneDrive/Desktop/School Code/GITC\pygame++')
from tilemap import Tilemap
from label import Label
from game_screen import Game_screen
from menu_screen import Menu_screen

class UI:
    pygame.init()
    def __init__(self,master) -> None:
        self._screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption("GITC")
        self.master = master
        self.map = []
        self.background_tile_map = Tilemap(self._screen,self.map)
    
    def make_screens(self,sprites):
        self.game_screens = {
            'normal': Game_screen(self._screen,sprites,[self.background_tile_map],[Label(self._screen,'Inventory',text_list=self.master.player.inventory,size=20,exact_pos=[10,TILE_SIZE*MAP_ROWS])]),
            'start': Menu_screen(self._screen,self.background_tile_map,'Welcome Adventurer',['Start Game','Load Previous Game','Exit']),
            'paused': Menu_screen(self._screen,self.background_tile_map,'Paused',['Start Server','Save and Exit','Continue'],opacity=180),
            'game_over': Menu_screen(self._screen,self.background_tile_map,'Game Over',['Respawn','Exit'])
        }
    