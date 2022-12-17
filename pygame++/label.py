import pygame
from constants import SCREEN_HEIGHT,SCREEN_WIDTH,WHITE,BLACK

class Label:

    def __init__(self,screen,text,pos,size = 50,color = WHITE) -> None:
        self.font = pygame.font.Font('freesansbold.ttf', size)
        self.label_text = self.font.render(text, True, color, BLACK)
        self.textRect = self.label_text.get_rect()
        self.textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + pos * 50)
        screen.blit(self.label_text, self.textRect)
