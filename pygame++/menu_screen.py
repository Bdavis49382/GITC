from label import Label
from config import GRAY
import pygame
class Menu_screen:

    def __init__(self,screen,background_tile_map,title,buttons,opacity = 100,background=GRAY) -> None:
        """A menu screen made up of a title and several buttons.
        screen: the pygame screen you are using
        title: the text you'd like to display at the top
        buttons: the text for all the buttons in order
        background: the background color of the screen"""
        self.screen = screen
        self.background = background
        self.background_tile_map = background_tile_map
        self.opacity = opacity
        self.title = Label(self.screen,title,0)
        self.buttons = []
        for (index,button_text) in enumerate(buttons):
            self.buttons.append(Label(self.screen,button_text,menu_pos=(index*.5)+1,size=20))
    
    def clicked_button(self):
        """Returns the text from the button the mouse is currently over"""
        mouse = pygame.mouse.get_pos()
        for button in self.buttons:
            if button.textRect.left <= mouse[0] <= button.textRect.right and button.textRect.top <= mouse[1] <= button.textRect.bottom:
                return button.text
    
    def draw(self):
        self.screen.fill(self.background)

        self.background_tile_map.draw(self.opacity)

        self.title.draw()

        for button in self.buttons:
            button.draw()
        
        pygame.display.flip()
