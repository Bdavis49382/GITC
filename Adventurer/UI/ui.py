import pygame
from constants import TILE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, GRAY,MAP_COLUMNS,MAP_ROWS,WHITE,BLACK,RED
import sys
sys.path.append('C:/Users/Bdude/OneDrive/Desktop/School Code/GITC\pygame++')
from tilemap import Tilemap
from label import Label
from menu_screen import Menu_screen

class UI:
    pygame.init()
    def __init__(self,master) -> None:
        self._screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption("GITC")
        self.master = master
        self.map = []
        self.background_tile_map = Tilemap(self._screen,self.map)
    

    
    def refresh_screen(self,sprites_list,game_state):
        self._screen.fill(GRAY)

        if game_state == 'normal':
            self.background_tile_map.draw_tiles()
            self.draw_footer()

            sprites_list.update()

            sprites_list.draw(self._screen)
        elif game_state == 'start':
            self.background_tile_map.draw_tiles(100)
            self.menu_screen = Menu_screen(self._screen,'Welcome Adventurer',['Start Game','Load Previous Game','Exit'])
        elif game_state == 'paused':
            self.background_tile_map.draw_tiles(180)
            self.menu_screen = Menu_screen(self._screen,'Paused',['Start Server','Save and Exit','Continue'])
        elif game_state == 'game_over':
            self.background_tile_map.draw_tiles(100)
            self.menu_screen = Menu_screen(self._screen,'Game Over',['Respawn'])

        pygame.display.flip()
    
    def draw_footer(self):
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render(f'Inventory:{",".join(self.master.player.inventory)}', True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.left = 10
        textRect.top = TILE_SIZE*MAP_ROWS
        self._screen.blit(text, textRect)