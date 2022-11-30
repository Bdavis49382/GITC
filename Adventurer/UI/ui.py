import json
import pygame
import constants
from constants import WHITE,BLACK,RED
from constants import TILE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, GRAY,MAP_COLUMNS,MAP_ROWS

class UI:
    pygame.init()
    def __init__(self,master) -> None:
        self._screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption("GITC")
        self.master = master
        self.map = []
    
    def refresh_screen(self,sprites_list):
        self._screen.fill(GRAY)

        self.draw_background()
        self.draw_footer()

        sprites_list.update()

        sprites_list.draw(self._screen)

        pygame.display.flip()
    
    def refresh_game_over_screen(self):
        self._screen.fill(GRAY)
        self.draw_background()
        
        font = pygame.font.Font('freesansbold.ttf', 50)
        text = font.render('Game Over', True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self._screen.blit(text, textRect)

        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render('Respawn', True, RED, BLACK)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + SCREEN_HEIGHT // 4)
        self._screen.blit(text, textRect)

        pygame.display.flip()
        
    def click_respawn(self):
        mouse = pygame.mouse.get_pos()
        return SCREEN_WIDTH//2-50 <= mouse[0] <= SCREEN_WIDTH//2+50 and SCREEN_HEIGHT//2+SCREEN_HEIGHT//4-20 <= mouse[1] <= SCREEN_HEIGHT//2+SCREEN_HEIGHT//4+20

    def draw_footer(self):
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render(f'Inventory:{",".join(self.master.player.inventory)}', True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.left = 10
        textRect.top = TILE_SIZE*MAP_ROWS
        self._screen.blit(text, textRect)

    def draw_background(self):
        tiles = {
            'floor': pygame.image.load('0x72_16x16DungeonTileset.v5/items/floor_plain.png').convert_alpha(),
            'wall': pygame.image.load('0x72_16x16DungeonTileset.v5/items/wall_left.png').convert_alpha()
        }
        for key in tiles:
            tiles[key] = pygame.transform.scale(tiles[key], (TILE_SIZE,TILE_SIZE))
        
        for y in range(MAP_ROWS):
            for x in range(MAP_COLUMNS):
                self._screen.blit(tiles[self.map[y][x]],(x*TILE_SIZE,y*TILE_SIZE))