from UI.ui import UI
from game.game_object import Game_object
from game.player import Player
from game.server import Server
from constants import ENTRANCE,MAP_COLUMNS,MAP_ROWS
import copy
import random
import json
import pygame

class Master:

    def __init__(self) -> None:
        self.load_files()
        self.server = Server({
            'rooms':self.rooms,
            'room':self.room,
            'maze':self.maze,
            'game_objects': self.saved_game_objects}
            )
        self.game_over = False
        self.GUI = UI()
        self.current_sprites_list = pygame.sprite.Group()
        self.player = Player((MAP_COLUMNS//2,MAP_ROWS//2),self)
        self.all_game_objects = {}
        for object_key in self.saved_game_objects:
            object = self.saved_game_objects[object_key]
            if object['type'] == 'Player':
                self.all_game_objects[object_key] = Player(object['maze_pos'],self)
                self.player = self.all_game_objects[object_key]
            elif object['type'] == 'Item':
                self.all_game_objects[object_key] = Game_object(object['maze_pos'],object['type'],name=object['name'],filename=f"0x72_16x16DungeonTileset.v5/items/{object['file_name']}.png")
            else:
                self.all_game_objects[object_key] = Game_object(object['maze_pos'],object['type'],filename=f"0x72_16x16DungeonTileset.v5/items/{object['file_name']}.png")
            
            if object['maze_pos'] == self.player.maze_pos:
                self.current_sprites_list.add(self.all_game_objects[object_key])

        self.new_room()
    
    def load_files(self):
        with open('Adventurer/UI/rooms.json','r') as room_file:
            rooms = json.load(room_file)
            self.rooms = rooms['rooms']
        with open('Adventurer/game/big_map.json','r') as map_file:
            data = json.load(map_file)
            self.room = data['room']
            self.maze = data['maze']
        with open('Adventurer/game/game_objects.json','r') as objects_file:
            self.saved_game_objects = json.load(objects_file)

    def new_room(self):
        room = copy.deepcopy(random.choice(self.rooms))
        # if self.server.conn:
        #     self.server.send(json.dumps({'player_maze_pos':self.player.maze_pos}),self.server.conn)
        self.make_doors(room,self.maze[self.player.maze_pos[1]][self.player.maze_pos[0]].split(','))
        self.server.data['game_objects']['player']['maze_pos'] = self.player.maze_pos
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
    

    def update_sprites_list(self):
        self.current_sprites_list = pygame.sprite.Group()
        for object_key in self.all_game_objects:
            if self.all_game_objects[object_key].maze_pos == self.player.maze_pos:
                self.current_sprites_list.add(self.all_game_objects[object_key])
                self.check_for_collisions(object_key)

    def check_for_collisions(self,object_key):
        if object_key != 'Player' and self.all_game_objects[object_key].tile_pos == self.player.tile_pos:
            match (self.all_game_objects[object_key].type):
                case 'Enemy':
                    print('Game Over')
                    self.game_over = True
                case 'Item':
                    print(f"You now have a {self.all_game_objects[object_key].name}")
                    self.all_game_objects[object_key].maze_pos = [-1,-1]
                    self.server.data['game_objects'][object_key]['maze_pos'] = [-1,-1]
                case 'Stairs':
                    print('You have made it to the next level')
                    self.player.maze_pos = [ 0 , 0]
                    self.new_room()

    
    def start_game(self):
        done = False
        clock = pygame.time.Clock()

        while not done:
            done = self.detect_events(pygame.event.get())
            if not self.game_over:
                self.update_sprites_list()
                self.GUI.refresh_screen(self.current_sprites_list)
            else:
                self.GUI.refresh_game_over_screen()



            clock.tick(60)
        pygame.quit()
    
        
        


