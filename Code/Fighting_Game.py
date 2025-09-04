import pygame
from Menu_Stack import MenuStack
from All_Menus import *


class FightingGame:
    def __init__(self):
        # Create the window
        self.screen = pygame.display.set_mode((1280,720))
        # Variable for game loop
        self.running = True
        # Sets window title
        pygame.display.set_caption("Fighting_game_window")
        # Initialise the menu stack and the first menu
        self.menu_stack = MenuStack()
        self.main_menu = MainMenu(self)
        # Push the first menu to the stack to be displayed
        self.menu_stack.push(self.main_menu)
        
    # calls the render method for the current menu on the top of the stack    
    def render(self):
        current_menu = self.menu_stack.peek()
        current_menu.render()
    
        
    # calls the top of stacks handle input method to check for escape/next menu transitions 
    def handle_input(self):
        current_menu = self.menu_stack.peek()
        current_menu.handle_input()
    
    # loop per frame
    def run(self):
    
        while self.running:
            # checks for input
            self.handle_input()
            # displays background & updates
            self.render()
            
        pygame.quit()
        
        

                    

        
        
                 
                 
                 
                 
                 
                 

    