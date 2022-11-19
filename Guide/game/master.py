from UI.ui import UI
from game.game_object import Game_object
from game.player import Player
from constants import ENTRANCE,MAP_COLUMNS,MAP_ROWS
import random
import json
import pygame

class Master:

    def __init__(self) -> None:
        self.rooms = self.load_file()
        self.GUI = UI()
        self.new_room()
        self.all_sprites_list = pygame.sprite.Group()
        player = Player((MAP_COLUMNS//2,MAP_ROWS//2),self)
        self.all_game_objects = {'player':player}
        self.all_sprites_list.add(player)
        self.all_sprites_list.add(Game_object((8,16)))
    
    def load_file(self):
        with open('Adventurer/UI/rooms.json','r') as room_file:
            rooms = json.load(room_file)
            return rooms['rooms']
    def new_room(self):
        room = random.choice(self.rooms)
        self.make_doors(room,['TOP','LEFT','BOTTOM'])
        self.map = room
        self.GUI.map = room

    
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
                            player.move_left(self.map)
                        case pygame.K_d:
                            player.move_right(self.map)
                        case pygame.K_w:
                            player.move_up(self.map)
                        case pygame.K_s:
                            player.move_down(self.map)

        return done
    


    def start_game(self):
        done = False
        clock = pygame.time.Clock()

        while not done:
            done = self.detect_events(pygame.event.get())
            self.GUI.refresh_screen(self.all_sprites_list)


            clock.tick(60)
        pygame.quit()
    
        
        


