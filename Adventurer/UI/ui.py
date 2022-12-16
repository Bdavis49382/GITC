import pygame
from UI.label import Label
from constants import TILE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, GRAY,MAP_COLUMNS,MAP_ROWS,WHITE,BLACK,RED
import sys
sys.path.append('C:/Users/Bdude/OneDrive/Desktop/School Code/GITC\pygame++')
from tilemap import Tilemap

class UI:
    pygame.init()
    def __init__(self,master) -> None:
        self._screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption("GITC")
        self.master = master
        self.map = []
        self.background_tile_map = Tilemap(self._screen,self.map)
    
    def refresh_start_screen(self):
        self._screen.fill(GRAY)
        self.background_tile_map.draw_tiles(100)

        title = Label(self._screen,'Welcome Adventurer',0)

        start_button = Label(self._screen,'Start Game',1,20)

        load_button = Label(self._screen,'Load Previous Game',1.5,20)

        exit_button = Label(self._screen,'Exit',2,20)

        pygame.display.flip()

    
    def refresh_screen(self,sprites_list,game_state):
        self._screen.fill(GRAY)

        self.background_tile_map.draw_tiles()
        self.draw_footer()

        sprites_list.update()

        sprites_list.draw(self._screen)

        pygame.display.flip()
    
    def refresh_game_over_screen(self):
        self._screen.fill(GRAY)
        
        self.background_tile_map.draw_tiles(100)
        
        title= Label(self._screen,'Game Over',0)

        respawn_button = Label(self._screen,'Respawn',1,20,color=RED)

        pygame.display.flip()
    
    def refresh_pause_screen(self):
        self._screen.fill(GRAY)
        self.background_tile_map.draw_tiles(180)

        title = Label(self._screen,'Paused',0,50)

        server_button = Label(self._screen,'Start Server',1,20)

        save_button = Label(self._screen,'Save and Exit',1.5,20)

        continue_button = Label(self._screen,'Continue',2,20)

        pygame.display.flip()
        
        
    def clicked_button1(self):
        mouse = pygame.mouse.get_pos()
        return SCREEN_WIDTH//2-50 <= mouse[0] <= SCREEN_WIDTH//2+50 and SCREEN_HEIGHT//2+40 <= mouse[1] <= SCREEN_HEIGHT//2+60

    def clicked_button2(self):
        mouse = pygame.mouse.get_pos()
        return SCREEN_WIDTH//2-50 <= mouse[0] <= SCREEN_WIDTH//2+50 and SCREEN_HEIGHT//2+65 <= mouse[1] <= SCREEN_HEIGHT//2+85
    
    def clicked_button3(self):
        mouse = pygame.mouse.get_pos()
        return SCREEN_WIDTH//2-50 <= mouse[0] <= SCREEN_WIDTH//2+50 and SCREEN_HEIGHT//2+90 <= mouse[1] <= SCREEN_HEIGHT//2+110

    def draw_footer(self):
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render(f'Inventory:{",".join(self.master.player.inventory)}', True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.left = 10
        textRect.top = TILE_SIZE*MAP_ROWS
        self._screen.blit(text, textRect)
