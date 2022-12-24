from constants import TILE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, GRAY,MAP_COLUMNS,MAP_ROWS,WHITE,BLACK,RED
import sys
sys.path.append('C:/Users/Bdude/OneDrive/Desktop/School Code/GITC\pygame++')
from components.tilemap import Tilemap
from components.label import Label
from screens.game_screen import Game_screen
from screens.menu_screen import Menu_screen
from screens.ui import UI

class UI(UI):
    def __init__(self,master) -> None:
        super().__init__()
        self.master = master
        self.map = []
        self.background_tile_map = Tilemap(self.screen,self.map)
    
    def make_screens(self,sprites):
        self.game_screens = {
            'normal': Game_screen(self.screen,sprites,[self.background_tile_map],[Label(self.screen,'Inventory',text_list=self.master.player.inventory,size=20,exact_pos=[10,TILE_SIZE*MAP_ROWS])]),
            'start': Menu_screen(self.screen,self.background_tile_map,'Welcome Adventurer',['Start Game','Load Previous Game','Exit']),
            'paused': Menu_screen(self.screen,self.background_tile_map,'Paused',['Start Server','Save and Exit','Continue'],opacity=180),
            'game_over': Menu_screen(self.screen,self.background_tile_map,'Game Over',['Respawn','Exit'])
        }
    