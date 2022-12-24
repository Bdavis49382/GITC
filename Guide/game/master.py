from UI.ui import UI
from game.game_object import Game_object
from game.player import Player
import sys
sys.path.append('C:/Users/Bdude/OneDrive/Desktop/School Code/GITC\pygame++')
from multiplayer.client import Client
from constants import ENTRANCE,MAP_COLUMNS,MAP_ROWS
import random
import json
import pygame

class Master:

    def __init__(self) -> None:
        self.client = Client()
        self.game_level = 0
        self.all_sprites_list = pygame.sprite.Group()
        self.GUI = UI(self,self.all_sprites_list,self.client)
        server_game_objects = self.client.send('rqst,game_objects')
        self.all_game_objects = {}
        for object_key in server_game_objects:
            object = server_game_objects[object_key]
            if object['type'] == 'Player':
                self.all_game_objects[object_key] = Player(object['maze_pos'],self)
            elif object['type'] == 'Item':
                self.all_game_objects[object_key] = Game_object(object['type'],object['maze_pos'],pos=1,filename=object['file_name'])
            else:
                self.all_game_objects[object_key] = Game_object(object['type'],object['maze_pos'],pos=2,filename=object['file_name'])
            
            self.all_sprites_list.add(self.all_game_objects[object_key])

        self.done = False
    

    
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
    
    def update_sprite_list(self):
        self.all_sprites_list = pygame.sprite.Group()
        for object_key in self.all_game_objects:
            self.all_sprites_list.add(self.all_game_objects[object_key])



    def start_game(self):
        clock = pygame.time.Clock()

        while not self.done:
            self.done = self.detect_events(pygame.event.get())
            self.update_sprite_list()
            self.GUI.game_screen.draw()
            self.update_values()

            clock.tick(30)
        self.client.send("!DISCONNECT")
        pygame.quit()
    
    def update_values(self):
        if self.client.send('rqst,still_running'):
            level = self.client.send('rqst,level')
            if level>self.game_level:
                self.all_game_objects = {}
                self.game_level = level
                

            server_game_objects = self.client.send('rqst,game_objects')
            

            for object_key in server_game_objects:
                if object_key in self.all_game_objects:
                    self.all_game_objects[object_key].update_maze_pos(server_game_objects[object_key]['maze_pos'])
                    self.all_game_objects[object_key].type = server_game_objects[object_key]['type']
                    if self.all_game_objects[object_key].file_name != server_game_objects[object_key]['file_name']:
                        self.all_game_objects[object_key].load_image(server_game_objects[object_key]['file_name'])
                    # if object_key == 'chest1':
                    #     print(self.all_game_objects[object_key].file_name)

                else:
                    self.all_game_objects[object_key] = Game_object(server_game_objects[object_key]['type'],server_game_objects[object_key]['maze_pos'],pos=2,filename=server_game_objects[object_key]['file_name'])
                    self.all_sprites_list.add(self.all_game_objects[object_key])
        else:
           self.done = True 
        