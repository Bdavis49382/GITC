from UI.ui import UI
from game.game_object import Game_object
from game.player import Player
import sys
sys.path.append('C:/Users/Bdude/OneDrive/Desktop/School Code/GITC\pygame++')
from multiplayer.server import Server
from constants import ENTRANCE,DEFAULT_POS
import copy
import random
import json
import pygame

class Master:

    def __init__(self) -> None:
        self.load_files()
        self.game_state = 'start'
        self.game_level = 0
        self.server = Server({
            'rooms':self.rooms,
            'room':self.room,
            'mazes':self.mazes,
            'game_objects': self.game_objects_by_level[0],
            'still_running':True,
            'level':0}
            )
        self.current_sprites_list = pygame.sprite.Group()
        self.GUI = UI(self)
        self.load_game_objects()
        self.GUI.make_screens(self.current_sprites_list)

        self.chest_rewards = ['Bomb','Torch']
        self.clock = 0

        self.keyboard_map = {
            pygame.K_a:'left',
            pygame.K_s:'down',
            pygame.K_d:'right',
            pygame.K_w:'up'}

        self.new_room()
    
    def load_game_objects(self,saved_game_objects=None):
        self.all_game_objects = {}
        if not saved_game_objects:
            saved_game_objects = self.game_objects_by_level[self.game_level]
        for object_key in saved_game_objects:
            object = saved_game_objects[object_key]
            if 'tile_pos' in object:
                pos = object['tile_pos']
            else:
                pos = DEFAULT_POS
            if object['type'] == 'Player':
                self.all_game_objects[object_key] = Player(object['maze_pos'],self,pos=pos)
                self.player = self.all_game_objects[object_key]
            elif object['type'] == 'Item':
                self.all_game_objects[object_key] = Game_object(object['maze_pos'],object['type'],name=object['name'],filename=object['file_name'])
            else:
                if 'path' in object:
                    self.all_game_objects[object_key] = Game_object(object['maze_pos'],object['type'],path=object['path'],filename=object['file_name'])
                else:
                    self.all_game_objects[object_key] = Game_object(object['maze_pos'],object['type'],filename=object['file_name'])
            if object['maze_pos'] == self.player.maze_pos:
                self.current_sprites_list.add(self.all_game_objects[object_key])
        
        self.server.data['game_objects'] = self.game_objects_by_level[self.game_level]

    def load_files(self):
        with open('Adventurer/UI/rooms.json','r') as room_file:
            rooms = json.load(room_file)
            self.rooms = rooms['rooms']
        with open('Adventurer/game/big_map.json','r') as map_file:
            data = json.load(map_file)
            self.room = data['room']
            self.mazes = data['mazes']
        with open('Adventurer/game/game_objects.json','r') as objects_file:
            self.game_objects_by_level = json.load(objects_file)["levels"]

    def new_room(self):
        room = copy.deepcopy(random.choice(self.rooms))
        self.player.path_taken.append(copy.deepcopy(self.player.maze_pos))
        self.make_doors(room,self.mazes[self.game_level][self.player.maze_pos[1]][self.player.maze_pos[0]].split(','))
        self.server.data['game_objects']['player']['maze_pos'] = self.player.maze_pos
        self.clock += 1
        if self.clock == 3:
            self.spawn_demon()

        self.move_objects_along_paths()                

        self.map = room
        self.GUI.background_tile_map.map = room
    
    def move_objects_along_paths(self):
        for object_key in self.all_game_objects:
            object = self.all_game_objects[object_key]
            if len(object.path) > 0 and object.maze_pos != self.player.maze_pos:
                if object.path_pos < len(object.path)-1:
                    object.path_pos += 1
                else:
                    object.path_pos = 0
                object.maze_pos = object.path[object.path_pos]
                if object_key in self.server.data['game_objects']:
                    self.server.data['game_objects'][object_key]['maze_pos'] = object.maze_pos
                else:
                    self.server.data['game_objects'][object_key] = object.to_dict()

    def spawn_demon(self):
        self.all_game_objects['demon'] = Game_object([0,0],'Enemy',path=self.player.path_taken,filename="monster_demon")
        self.server.data['game_objects']['demon'] = self.all_game_objects['demon'].to_dict()

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
                    self.server.data['still_running'] = False
                case pygame.KEYDOWN:
                    if event.key in self.keyboard_map:
                        player.current_direction = self.keyboard_map[event.key]
                        player.move(self.map)
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = 'paused' if self.game_state != 'paused' else 'normal'
                case pygame.KEYUP:
                    if event.key in self.keyboard_map:
                        if self.keyboard_map[event.key] == player.current_direction:
                            player.current_direction = 'none'

                case pygame.MOUSEBUTTONDOWN:
                    match self.GUI.game_screens[self.game_state].clicked_button():
                        case 'Respawn':
                            self.restart_game()
                        case 'Start Server':
                            self.server.launch()
                        case 'Save and Exit':
                            done = True
                            self.server.data['still_running'] = False
                            self.save_game()
                        case 'Continue':
                            self.game_state = 'normal'
                        case 'Start Game':
                            self.game_state = 'normal'
                        case 'Load Previous Game':
                            self.load_game()
                            self.game_state = 'normal'
                        case 'Exit':
                            done = True
        return done
    
    def load_game(self):
        with open('Adventurer/game/saved_game_objects.json') as save_file:
            saved_data = json.load(save_file)
            # self.saved_game_objects = saved_data['game_objects']
            self.load_game_objects(saved_game_objects=saved_data['game_objects'])
            self.new_room()
            self.player.inventory = saved_data['inventory']
    
    def restart_game(self):
        self.load_files()
        self.all_game_objects = {}
        self.load_game_objects()
        if 'demon' in self.server.data['game_objects']:
            self.server.data['game_objects']['demon']['maze_pos'] = [-1 ,-1]
        
        self.game_state = 'normal'
        self.chest_rewards = ['Bomb','Torch']
        self.clock = 0
        self.new_room()
    
    def update_sprites_list(self):
        self.current_sprites_list = pygame.sprite.Group()
        for object_key in self.all_game_objects:
            if self.all_game_objects[object_key].maze_pos == self.player.maze_pos:
                self.current_sprites_list.add(self.all_game_objects[object_key])
                if self.handle_collisions(object_key):
                    break
        self.GUI.game_screens['normal'].sprites = self.current_sprites_list

    def handle_collisions(self,object_key):
        if object_key != 'Player' and self.all_game_objects[object_key].tile_pos == self.player.tile_pos:
            match (self.all_game_objects[object_key].type):
                case 'Enemy':
                    print('Game Over')
                    self.game_state = 'game_over'
                case 'Item':
                    name = self.all_game_objects[object_key].name
                    print(f"You now have a {name}")
                    self.player.inventory.append(name)
                    self.all_game_objects[object_key].maze_pos = [-1,-1]
                    self.server.data['game_objects'][object_key]['maze_pos'] = [-1,-1]
                case 'Stairs':
                    print('You have made it to the next level')
                    self.next_level()
                    return True
                case 'Closed_chest':
                    self.player.inventory.append(random.choice(self.chest_rewards))
                    self.all_game_objects[object_key] = Game_object(self.all_game_objects[object_key].maze_pos,'Open_chest',filename="chest_open_empty")
                    self.server.data['game_objects'][object_key] = self.all_game_objects[object_key].to_dict()
                    
    def save_game(self):
        with open('Adventurer/game/saved_game_objects.json','w') as write_file:
            all_game_objects_data = {}
            for object_key in self.all_game_objects:
                object = self.all_game_objects[object_key]
                all_game_objects_data[object_key] = object.to_dict()
            save_data = {'inventory':self.player.inventory,'game_objects':all_game_objects_data}
            write_file.write(json.dumps(save_data))
    
    def next_level(self):
        self.game_level += 1
        self.load_game_objects()
        self.server.data['level'] += 1
        self.server.data['game_objects'] = self.game_objects_by_level[self.game_level]
        self.new_room()
    
    def start_game(self):
        done = False
        clock = pygame.time.Clock()

        while not done:
            done = self.detect_events(pygame.event.get())
            if self.game_state == 'normal':
                self.update_sprites_list()
            self.GUI.game_screens[self.game_state].draw()
            # self.player.move(self.map)
            
            clock.tick(60)
        pygame.quit()