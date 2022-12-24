import pygame
from config import SCREEN_HEIGHT,SCREEN_WIDTH,WHITE,BLACK

class Label:

    def __init__(self,screen,text,exact_pos = None,menu_pos = 0,size = 50,color = WHITE,background = BLACK,text_list=None) -> None:
        """Puts a label with text on the screen.
        Parameters:
        screen: the pygame screen it will be blitted onto
        text: the desired text to be displayed
        exact_pos: the x and y coordinates of the label. If omitted, will default to center of the screen
        menu_pos: An integer that puts it in a slot of a menu, automatically 0, which is the center of the screen
        size: the size of the text
        color: the color of the text
        background: the color of the rectangle around the text
        text_list: If the information to be displayed is a list, put a reference to the list here. The text would then be the title for the list"""
        self.text = text
        self.text_list = text_list
        self.font = pygame.font.Font('freesansbold.ttf', size)
        self.color = color
        self.background = background
        self.label_text = self.font.render(text, True, color, background)
        self.textRect = self.label_text.get_rect()
        if not exact_pos:
            self.textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + menu_pos * 50)
        else:
            self.textRect.topleft = exact_pos
        self.screen = screen
    
    def draw(self):
        if self.text_list:
            self.label_text = self.font.render(f'{self.text}: {", ".join(self.text_list)}', True, self.color, self.background)
        self.screen.blit(self.label_text,self.textRect)
