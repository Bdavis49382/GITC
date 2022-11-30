from UI.ui import UI
from game.game_object import Game_object
from game.player import Player
from game.client import Client
from constants import ENTRANCE,MAP_COLUMNS,MAP_ROWS,ITEM_FILE_PATH
import random
import json
import pygame

class Master:

    def __init__(self) -> None:
        self.client = Client()
        self.GUI = UI(self,self.client)
        self.all_sprites_list = pygame.sprite.Group()
        server_game_objects = self.client.send('rqst,game_objects')
        self.all_game_objects = {}
        for object_key in server_game_objects:
            object = server_game_objects[object_key]
            if object['type'] == 'Player':
                self.all_game_objects[object_key] = Player(object['maze_pos'],self)
            elif object['type'] == 'Item':
                self.all_game_objects[object_key] = Game_object(object['maze_pos'],pos=1,filename=f"0x72_16x16DungeonTileset.v5/items/{object['file_name']}.png")
            else:
                self.all_game_objects[object_key] = Game_object(object['maze_pos'],pos=2,filename=f"0x72_16x16DungeonTileset.v5/items/{object['file_name']}.png")
            
            self.all_sprites_list.add(self.all_game_objects[object_key])
    

    
    def make_doors(self,room,entrances):
        for entrance in entrances:
            x,y = ENTRANCE[entrance]
            room[y][x] = 'floor'

    def detect_events(self,events):
        done = False
        player = self.all_game_objects['player']
        for event in events:
            match event.type:
                case pygame.QUIT:
                    done = True
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_x:
                            done = True
                        case pygame.K_a:
                            pass
                        case pygame.K_d:
                            pass
                        case pygame.K_w:
                            pass
                        case pygame.K_s:
                            pass

        return done
    


    def start_game(self):
        done = False
        clock = pygame.time.Clock()

        while not done:
            done = self.detect_events(pygame.event.get())
            self.GUI.refresh_screen(self.all_sprites_list)
            self.update_values()

            clock.tick(30)
        self.client.send("!DISCONNECT")
        pygame.quit()
    
    def update_values(self):
        server_game_objects = self.client.send('rqst,game_objects')
        for object_key in self.all_game_objects:
            self.all_game_objects[object_key].update_maze_pos(server_game_objects[object_key]['maze_pos'])
    
        