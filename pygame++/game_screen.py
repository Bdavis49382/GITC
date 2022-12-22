from config import GRAY
import pygame

class Game_screen:
    def __init__(self,screen,sprites,tilemaps,labels,background=GRAY) -> None:
        self.screen = screen
        self.background = background
        self.tilemaps = tilemaps
        self.labels = labels
        self.sprites = sprites
    
    def draw(self):
        self.screen.fill(self.background)

        for tilemap in self.tilemaps:
            tilemap.draw()
        
        self.sprites.update()
        self.sprites.draw(self.screen)

        for label in self.labels:
            label.draw()
        
        pygame.display.flip()
