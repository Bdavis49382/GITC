from label import Label
import pygame
class Menu_screen:

    def __init__(self,screen,title,buttons) -> None:
        self.screen = screen
        self.title = Label(self.screen,title,0)
        self.buttons = []
        for (index,button_text) in enumerate(buttons):
            self.buttons.append(Label(self.screen,button_text,(index*.5)+1,20))
    
    def clicked_button(self):
        mouse = pygame.mouse.get_pos()
        for (button_num,button) in enumerate(self.buttons):
            if button.textRect.left <= mouse[0] <= button.textRect.right and button.textRect.top <= mouse[1] <= button.textRect.bottom:
                return button_num
