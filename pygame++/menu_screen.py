from label import Label
import pygame
class Menu_screen:

    def __init__(self,screen,title,buttons) -> None:
        """A menu screen made up of a title and several buttons.
        screen: the pygame screen you are using
        title: the text you'd like to display at the top
        buttons: the text for all the buttons in order"""
        self.screen = screen
        self.title = Label(self.screen,title,0)
        self.buttons = []
        for (index,button_text) in enumerate(buttons):
            self.buttons.append(Label(self.screen,button_text,(index*.5)+1,20))
    
    def clicked_button(self):
        """Returns the text from the button the mouse is currently over"""
        mouse = pygame.mouse.get_pos()
        for button in self.buttons:
            if button.textRect.left <= mouse[0] <= button.textRect.right and button.textRect.top <= mouse[1] <= button.textRect.bottom:
                return button.text
