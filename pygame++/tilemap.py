from config import TEXTURE_REFERENCE, MAP_COLUMNS, MAP_ROWS, MAP_KEY, TILE_SIZE
import pygame

class Tilemap:
    def __init__(self,screen,map,tile_size = TILE_SIZE,map_key = MAP_KEY,opacity=255,offset=[0,0],size=[MAP_COLUMNS,MAP_ROWS]) -> None:
        """Takes five parameters to create a background tilemap. 
        map: a two dimensional array of words that represent textures, such as wall or floor
        tile_size: the size of the tiles being used for this particular screen if you don't want to use the size in the config file
        map_key: a dictionary matching the words in the map with actual file names, if not provided, one from the config file will be used
        opacity: the opacity you want the textures to be displayed at, if not provided, full opacity will be used
        offset: If you don't want the tilemap to start in the top left corner of the screen, enter an x and y value here
        size: Set the number of columns and rows you want, or it will default to what's in the config file
        """
        self.tiles = {}
        self.size = size
        self.map = map
        self.map_key = map_key
        self.tile_size = tile_size
        self.opacity = opacity
        self.screen = screen
        self.offset = offset
        self._load_tiles()
    
        
    def draw_tiles(self,opacity=255):
        """Actually draw the tilemap to the screen, optionally specify an opacity less than 255"""

        if self.opacity != opacity:
            self._set_opacity(opacity)

        for y in range(self.size[1]):
            for x in range(self.size[0]):
                self.screen.blit(self.tiles[self.map[y][x]],(x*self.tile_size+self.offset[0],y*self.tile_size+self.offset[1]))
    
    def _set_opacity(self,new_opacity):
        """Change the opacity of all tiles for the tilemap"""
        self.opacity = new_opacity
        for tile in self.tiles:
            self.tiles[tile].set_alpha(self.opacity)

    def _load_tiles(self):
        """Use the key to load the images into self.tiles"""
        for tile in self.map_key:
            self.tiles[tile] = pygame.image.load(TEXTURE_REFERENCE.format(self.map_key[tile])).convert_alpha()
            self.tiles[tile] = pygame.transform.scale(self.tiles[tile], (self.tile_size,self.tile_size))
            self.tiles[tile].set_alpha(self.opacity)
        

    