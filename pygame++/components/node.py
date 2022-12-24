from config import WHITE,TILE_SIZE,DEFAULT_POS,TEXTURE_REFERENCE
import pygame
class Node(pygame.sprite.Sprite):

    def __init__(self,type,name='',tile_pos=DEFAULT_POS,filename='',tile_size=TILE_SIZE) -> None:
        """A node is an object on the screen. An extension of pygame.sprite, it uses a tile-based system and a 
        texture reference from the config to create an object which can be drawn on the screen.
        type: the type of object is is, EX: item, enemy, player
        name: the name of the specific object, if necessary
        tile_pos: the x and y position by tiles of the object. Takes a default position from the config file
        file_name: the name of the specific file for the texture. NOTE: Doesn't require the whole path. Uses TEXTURE_REFERENCE
        from the config file.
        tile_size: if the tile_size needs to be different from the config file for any reason, this can be changed here"""
        super().__init__()

        self.tile_size = tile_size
        self.type = type
        self.name = name

        self.file_name = filename
        self.tile_pos = tile_pos

        self.load_image(filename)

    
    def load_image(self,filename):
        if filename != '':
            self.image = pygame.image.load(TEXTURE_REFERENCE.format(filename)).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.tile_size,self.tile_size))
            self.rect = self.image.get_rect()
        else:
            self.image = pygame.Surface([self.tile_size,self.tile_size])
            self.image.fill(WHITE)
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()
        self.rect.x = self.tile_pos[0]*self.tile_size
        self.rect.y = self.tile_pos[1]*self.tile_size


