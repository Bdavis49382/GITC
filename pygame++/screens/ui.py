from config import SCREEN_HEIGHT,SCREEN_WIDTH,GAME_TITLE
import pygame
class UI:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)