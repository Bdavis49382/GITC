from UI.ui import UI
from game.game_object import Game_object
from game.player import Player
import sys
sys.path.append('C:/Users/Bdude/OneDrive/Desktop/School Code/GITC\pygame++')
from server import Server
from constants import ENTRANCE,MAP_COLUMNS,MAP_ROWS,DEFAULT_POS,TEXTURE_REFERENCE
import copy
import random
import json
import pygame

class Master:

    def __init__(self) -> None:
        self.load_files()
        self.game_state = 'start'
        self.server = None  # TODO: change this so it can collect data but launch later
        self.GUI = UI(self)
        self.current_sprites_list = pygame.sprite.Group()
        self.all_game_objects = {}
        self.load_game_objects()

        self.chest_rewards = ['Bomb','Torch']
        self.clock = 0

        self.new_room()
    
    def load_game_objects(self):
        for object_key in self.saved_game_objects:
            object = self.saved_game_objects[object_key]
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

    
    def launch_server(self):
        self.server = Server({
            'rooms':self.rooms,
            'room':self.room,
            'maze':self.maze,
            'game_objects': self.saved_game_objects,
            'still_running':True}
            )

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
        self.player.path_taken.append(copy.deepcopy(self.player.maze_pos))
        self.make_doors(room,self.maze[self.player.maze_pos[1]][self.player.maze_pos[0]].split(','))
        if self.server:
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
                if self.server:
                    if object_key in self.server.data['game_objects']:
                        self.server.data['game_objects'][object_key]['maze_pos'] = object.maze_pos
                    else:
                        self.server.data['game_objects'][object_key] = {'type':object.type,
                                                                'file_name':object.file_name,
                                                                'maze_pos':object.maze_pos,
                                                                'path':object.path} #might have bug later with objects that don't have a path but will work for now.


    def spawn_demon(self):
        self.all_game_objects['demon'] = Game_object([0,0],'Enemy',path=self.player.path_taken,filename="monster_demon")
        if self.server:
            self.server.data['game_objects']['demon'] = {'type':'Enemy',
                                                    'file_name':'monster_demon',
                                                    'maze_pos':[0,0],
                                                    'path':self.player.path_taken}
        
    
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
                    if self.server:
                        self.server.data['still_running'] = False
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
                        case pygame.K_ESCAPE:
                            self.game_state = 'paused' if self.game_state != 'paused' else 'normal'
                case pygame.MOUSEBUTTONDOWN:
                    if self.GUI.clicked_button1() and self.game_state == 'game_over':
                        self.restart_game()
                    elif self.game_state == 'paused':
                        if self.GUI.clicked_button1():
                            self.launch_server()
                        elif self.GUI.clicked_button2():
                            done = True
                            if self.server:
                                self.server.data['still_running'] = False
                            self.save_game()
                        elif self.GUI.clicked_button3():
                            self.game_state = 'normal'
                    elif self.game_state == 'start':
                        if self.GUI.clicked_button1():
                            self.game_state = 'normal'
                        elif self.GUI.clicked_button2():
                            with open('Adventurer/game/saved_game_objects.json') as save_file:
                                saved_data = json.load(save_file)
                                self.saved_game_objects = saved_data['game_objects']
                                self.load_game_objects()
                                self.new_room()
                                self.player.inventory = saved_data['inventory']
                            self.game_state = 'normal'
                        elif self.GUI.clicked_button3():
                            done = True
                    
                            

        return done
    
    def restart_game(self):
        self.load_files()
        self.all_game_objects = {}
        for object_key in self.saved_game_objects:
            object = self.saved_game_objects[object_key]
            if object['type'] == 'Player':
                self.all_game_objects[object_key] = Player(object['maze_pos'],self)
                self.player = self.all_game_objects[object_key]
            elif object['type'] == 'Item':
                self.all_game_objects[object_key] = Game_object(object['maze_pos'],object['type'],name=object['name'],filename=TEXTURE_REFERENCE.format(object['file_name']))
            else:
                if 'path' in object:
                    self.all_game_objects[object_key] = Game_object(object['maze_pos'],object['type'],path=object['path'],filename=TEXTURE_REFERENCE.format(object['file_name']))
                else:
                    self.all_game_objects[object_key] = Game_object(object['maze_pos'],object['type'],filename=TEXTURE_REFERENCE.format(object['file_name']))
            
            if object['maze_pos'] == self.player.maze_pos:
                self.current_sprites_list.add(self.all_game_objects[object_key])
        if self.server:
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
                self.handle_collisions(object_key)

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
                    if self.server:
                        self.server.data['game_objects'][object_key]['maze_pos'] = [-1,-1]
                case 'Stairs':
                    print('You have made it to the next level')
                    self.player.maze_pos = [ 0 , 0]
                    self.new_room()
                case 'Closed_chest':
                    self.player.inventory.append(random.choice(self.chest_rewards))
                    self.all_game_objects[object_key] = Game_object(self.all_game_objects[object_key].maze_pos,'Open_chest',filename="chest_open_empty")
                    if self.server:
                        self.server.data['game_objects'][object_key]['file_name'] = 'chest_open_empty'
                        self.server.data['game_objects'][object_key]['type'] = 'Open_chest'
                    
    def save_game(self):
        with open('Adventurer/game/saved_game_objects.json','w') as write_file:
            all_game_objects_data = {}
            for object_key in self.all_game_objects:
                object = self.all_game_objects[object_key]
                all_game_objects_data[object_key] = {
                    'type':object.type,
                    'maze_pos':object.maze_pos,
                    'path':object.path,
                    'file_name':object.file_name,
                    'name':object.name,
                    'tile_pos':object.tile_pos
                }
            save_data = {'inventory':self.player.inventory,'game_objects':all_game_objects_data}
            write_file.write(json.dumps(save_data))
    
    def start_game(self):
        done = False
        clock = pygame.time.Clock()

        while not done:
            done = self.detect_events(pygame.event.get())
            if self.game_state == 'normal':
                self.update_sprites_list()
                self.GUI.refresh_screen(self.current_sprites_list,self.game_state)
            elif self.game_state == 'paused':
                self.GUI.refresh_pause_screen()
            elif self.game_state == 'game_over':
                self.GUI.refresh_game_over_screen()
            elif self.game_state == 'start':
                self.GUI.refresh_start_screen()

            clock.tick(60)
        pygame.quit()
    