import pygame
import os
import threading

from GameLoop import *
from Lobby_Client import LobbyClient
from StatTable import HashTable


# Base screen class each menu inherits from
class GeneralMenu:
    def __init__(self,game):
        # allows the game object to be referenced
        self.game = game
        # stores the path to the current working directory
        self.cur_dir = os.getcwd()
        # stores the parent directory to the current working directory
        self.parent_dir = os.path.dirname(self.cur_dir)
        # creates a new path to the screens directory, this works for all file structures for any machine
        self.screens_path = os.path.join(str(self.parent_dir),"Screens")
        self.opt_height = 52
    
    
    # handles the input for quitting and going back a screen
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # pops off the current screen, returning to the last one
                    self.game.menu_stack.pop_off()
            # calls the function for handling transitions to the next screen
            self.check_menu_transition(event)
     
    # code that will be overrided depending on the screen
    def check_menu_transition(self,event):
        pass
    
    
    # Function that takes in mouse pos and a rectangle
    # Then detects if mouse is within that rectangle
    def check_opt_press(self,mouse_pos,target_rect):
        # mouse_pos = tuple(x,y) positions
        # checks if mouse position within the width of the rectangle
        if mouse_pos[0] >= target_rect.x and mouse_pos[0] <= target_rect.x + target_rect.width:
            # checks if mouse position within the height of the rectangle
            if mouse_pos[1] >= target_rect.y and mouse_pos[1] <= target_rect.y + target_rect.height:
                return True
            else:
                return False
        else:
            return False




class MainMenu(GeneralMenu):
    def __init__(self,game):
        # initialises the superclass attributes
        super().__init__(game)
        # creates the image dependent relative path
        self.image_name = "main_menu_background.png"
        self.image_path = os.path.join(str(self.screens_path),self.image_name)
        # loads the image to a variable to be displayed
        self.background = pygame.image.load(self.image_path)
        # height of all options
        
        # initialise the rectangles for each option with their x,y,width and height
        self.play_rect = pygame.Rect(1073,149,191,self.opt_height)
        self.tutorial_rect = pygame.Rect(889,249,374,self.opt_height)
        self.stats_rect = pygame.Rect(14,382,233,self.opt_height)
        self.quit_rect = pygame.Rect(14,487,190,self.opt_height)
        
     
     # overrides the render method to display the different background
    def render(self):
        self.game.screen.blit(self.background,(0,0))
        pygame.display.flip()
                    
                   
    def check_menu_transition(self,event):
        # retrieves current mouse pos as tuple(x,y)
        cur_mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            # checks if option clicked, if so initialise new menu and push
            if self.check_opt_press(cur_mouse_pos,self.play_rect):
                play_menu = PlayMenu(self.game)
                self.game.menu_stack.push(play_menu)
                
            if self.check_opt_press(cur_mouse_pos,self.tutorial_rect):
                controls_screen = ControlsScreen(self.game)
                self.game.menu_stack.push(controls_screen)
                
            if self.check_opt_press(cur_mouse_pos,self.stats_rect):
                stats_menu = StatsMenu(self.game)
                self.game.menu_stack.push(stats_menu)
                
            if self.check_opt_press(cur_mouse_pos,self.quit_rect):
                self.game.running = False
           
                
  
            
class StatsMenu(GeneralMenu):
    def __init__(self,game):
        super().__init__(game)
        self.image_name = "stats_background.png"
        self.stats = HashTable()
        self.image_path = os.path.join(str(self.screens_path),self.image_name)
        self.background = pygame.image.load(self.image_path)
        self.displayed = False
        pygame.font.init()
        self.font = pygame.font.Font(None, 80)
        
    def display_stats(self):

        stat_y = 60
        table_data = self.stats.get_table()
        
        # loops through the hash table data
        # displays each stat pair on a new line
        
        for field in table_data:
            if field != None:
                for stat_pair in field:
                    stat_name = stat_pair[0]
                    stat_val = stat_pair[1]
                    stat_y += 60
                  
                    self.draw_stat_pair(stat_name,stat_val,stat_y)
                      
  
    def draw_stat_pair(self,stat_name,value,current_y):
        # renders the stat name and value
        
        stat_name_text = self.font.render(f"{stat_name.upper()}",True,(255,255,255))
        self.game.screen.blit(stat_name_text,(40,current_y))
        
        stat_val_text = self.font.render(f"{value}",True,(255,255,255))
        self.game.screen.blit(stat_val_text,(1100,current_y))
        
    def render(self):
        # only renders once as no updates required in stat menu
        if self.displayed == False:
            self.game.screen.blit(self.background,(0,0))
            self.display_stats()
            pygame.display.flip()
            self.displayed = True
        
        
        
                          
class PlayMenu(GeneralMenu):
    def __init__(self,game):
        super().__init__(game)
        self.image_name = "play_menu_background.png"
        self.image_path = os.path.join(str(self.screens_path),self.image_name)
        self.background = pygame.image.load(self.image_path)
        # option rects
        self.play_online_rect = pygame.Rect(369,177,493,self.opt_height)
        self.play_offline_rect = pygame.Rect(344,423,542,self.opt_height)
        
    def render(self):
        self.game.screen.blit(self.background,(0,0))
        pygame.display.flip()
                
    def check_menu_transition(self,event):
        # retrieves current mouse pos as tuple(x,y)
        cur_mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            # checks if option clicked, if so initialise new menu and push
            
            if self.check_opt_press(cur_mouse_pos,self.play_online_rect):
                play_online_menu = PlayOnlineMenu(self.game)
                self.game.menu_stack.push(play_online_menu)
            
            
            if self.check_opt_press(cur_mouse_pos,self.play_offline_rect):
                play_offline_menu = PlayOfflineMenu(self.game)
                self.game.menu_stack.push(play_offline_menu)
     
class ControlsScreen(GeneralMenu):
    def __init__(self,game):
        super().__init__(game)
        self.image_name = "controls_background.png"
        self.image_path = os.path.join(str(self.screens_path),self.image_name)
        self.background = pygame.image.load(self.image_path)
        self.rules_opt = pygame.Rect(940,640,210,50)
        
    def render(self):
        self.game.screen.blit(self.background,(0,0))
        pygame.display.flip()
        
        
    def check_menu_transition(self,event):
        
        # retrieves current mouse pos as tuple(x,y)
        cur_mouse_pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONUP:
            if self.check_opt_press(cur_mouse_pos,self.rules_opt):
                rules_screen = RulesScreen(self.game)
                self.game.menu_stack.push(rules_screen)
            
                       
class RulesScreen(GeneralMenu):
    
    def __init__(self,game):
        super().__init__(game)
        self.image_name = "rules_background.png"
        self.image_path = os.path.join(str(self.screens_path),self.image_name)
        self.background = pygame.image.load(self.image_path)
        
    def render(self):
        self.game.screen.blit(self.background,(0,0))
        pygame.display.flip()
        
    

class PlayOfflineMenu(GeneralMenu):
    def __init__(self,game):
        super().__init__(game)
        self.image_name = "play_offline_menu_background.png"
        self.image_path = os.path.join(str(self.screens_path),self.image_name)
        self.background = pygame.image.load(self.image_path)
        # option rect
        self.vs_ai_rect = pygame.Rect(488,212,218,self.opt_height)
        self.couch_coop_rect = pygame.Rect(384,421,445,self.opt_height)
        
    def render(self):
        self.game.screen.blit(self.background,(0,0))
        pygame.display.flip()
        
    def check_menu_transition(self,event):
        # retrieves current mouse pos as tuple(x,y)
        cur_mouse_pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONUP:
            
            # checks if option clicked, if so initialise new menu and push
            if self.check_opt_press(cur_mouse_pos,self.vs_ai_rect):
                ai_difficulty_menu = AiDifficultyMenu(self.game)
                self.game.menu_stack.push(ai_difficulty_menu)
                
            if self.check_opt_press(cur_mouse_pos,self.couch_coop_rect):
                character_select_menu = CharacterSelectMenu(self.game)
                self.game.menu_stack.push(character_select_menu)


class PlayOnlineMenu(GeneralMenu):
    def __init__(self,game):
        super().__init__(game)
        self.image_name = "lobby_menu.png"
        self.image_path = os.path.join(str(self.screens_path),self.image_name)
        self.background = pygame.image.load(self.image_path)
        self.host_rect = pygame.Rect(1043,16,211,57)
        # instantiate new client object and connect to server
        self.lobby_client  = LobbyClient()
        self.lobby_client.connect()
        self.hosting = False
        self.joined = False
        self.lobby_started = False
        # intialise font for displaying text
        pygame.font.init()
        self.font = pygame.font.Font(None, 100)
           
    def render(self):
        self.game.screen.blit(self.background,(0,0))
        # call for lobby data to be requested every 2 seconds
        self.lobby_client.check_lobby_update()
        # update the lobby visuals
        self.update_lobby(self.game.screen)
        # update top left to show FULL if 6 lobbies made
        self.display_full_text(self.game.screen)
        
        pygame.display.flip()
        
    def display_full_text(self,screen):
        full = self.lobby_client.max_lobbies_reached()
        if full:
             full_text = self.font.render("FULL",True,(255,0,0))
             screen.blit(full_text,(50,20))
            
               
    # override parent function so that client disconnects when exiting the menu
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # disconnects the client before leaving screen
                    self.lobby_client.close_connection()
                    self.game.menu_stack.pop_off()
                        
        
            self.host_lobby(event)
            self.handle_join_button_input(event)
                
        self.check_menu_transition()
                
                
    def check_menu_transition(self):
        client_id = self.lobby_client.get_client_id()
        
        # loops through the lobby dictionary 
        for lobby_id,lobby_info in self.lobby_client.get_lobby_data().items():
            # if clients id is in a lobby with 2 players (full), start the game
            if client_id in lobby_info["players"] and len(lobby_info["players"]) == 2 and self.lobby_started == False:
                # assigns player number, host is always player 1
                if lobby_info["players"][0] == client_id:
                    player_num = 1
                else:
                    player_num = 2
                 
                self.lobby_started = True
                
                char_select = OnlineCharacterSelectMenu(self.game,player_num,self.lobby_client,lobby_id)
                self.game.menu_stack.push(char_select)
                    
     
        
    def host_lobby(self,event):
        # retrieves current mouse pos as tuple(x,y)
        cur_mouse_pos = pygame.mouse.get_pos()
        max_lobbies = self.lobby_client.max_lobbies_reached()
        
        if event.type == pygame.MOUSEBUTTONUP:
            if self.check_opt_press(cur_mouse_pos,self.host_rect) and not self.hosting and not max_lobbies:
                host_request = self.lobby_client.host_game()
                if host_request.lower() == "received":
                    self.hosting = True
                     
    def update_lobby(self,screen):
        lobby_data = self.lobby_client.get_lobby_data()
        # properties for each lobby rect
        LOBBY_X = 64
        LOBBY_Y = 139
        LOBBY_WIDTH = 1168
        LOBBY_HEIGHT = 70
        
        
        # loops through the data and creates a new lobby rect for each lobby there is
        for lobby_id, lobby_info in lobby_data.items():
            # Creates the lobby rect for the current Y value and draw it white
            lobby_rect = pygame.Rect( LOBBY_X ,LOBBY_Y ,LOBBY_WIDTH, LOBBY_HEIGHT)
            pygame.draw.rect(screen,(255,255,255),lobby_rect)            
            # displays the lobby id number on the right of the rect
            lobby_number = self.font.render(str(lobby_id), True, (0, 255, 0))
            screen.blit(lobby_number,(LOBBY_X+10,LOBBY_Y))
            # calculates number of players in lobby
            player_count = len(lobby_info["players"])
            # displays player count on the lobby
            player_count_text = self.font.render(f"{player_count}/2",True,(0,255,0))    
            screen.blit(player_count_text,(LOBBY_X+ 1050,LOBBY_Y))
            self.draw_join_text(player_count,LOBBY_Y,screen)            
            # displays the join button if a place is free
            LOBBY_Y += 80
            
            
            
    def handle_join_button_input(self,event):
        cur_mouse_pos = pygame.mouse.get_pos()
        LOBBY_Y = 139
        JOIN_X = 524        
        for lobby_id, lobby_info in self.lobby_client.get_lobby_data().items():         
            player_count = len(lobby_info["players"])          
            if player_count == 1:
                join_rect = pygame.Rect(JOIN_X, LOBBY_Y, 150, 70)
                if event.type == pygame.MOUSEBUTTONUP:             
                    if self.check_opt_press(cur_mouse_pos, join_rect) and not self.joined and not self.hosting:
                        self.joined = True
                        self.lobby_client.join_game(lobby_id)
                        
            LOBBY_Y += 80
            
    def draw_join_text(self,player_count,current_y,screen):
        JOIN_X = 524
        if player_count == 1 and not self.hosting:
            join_text = self.font.render("JOIN",True,(0,255,0))
            screen.blit(join_text,(JOIN_X,current_y))
            
            
            
            
       
class AiDifficultyMenu(GeneralMenu):
    def __init__(self,game):
        super().__init__(game)
        self.image_name = "difficulty_ai_menu_background.png"
        self.image_path = os.path.join(str(self.screens_path),self.image_name)
        self.background = pygame.image.load(self.image_path)
        self.easy_rect= pygame.Rect(526,196,183,self.opt_height)
        self.hard_rect = pygame.Rect(526,451,183,self.opt_height)
        
    def render(self):
        self.game.screen.blit(self.background,(0,0))
        pygame.display.flip()
        
    def check_menu_transition(self,event):
        # retrieves current mouse pos as tuple(x,y)
        cur_mouse_pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONUP:
            
            # checks if option clicked, if so initialise new menu and push
            if self.check_opt_press(cur_mouse_pos,self.easy_rect):
                character_select_menu = CharacterSelectMenu(self.game,"easy")
                self.game.menu_stack.push(character_select_menu)
                
            if self.check_opt_press(cur_mouse_pos,self.hard_rect):
                character_select_menu = CharacterSelectMenu(self.game,"hard")
                self.game.menu_stack.push(character_select_menu)
        
        
        
        
        
class CharacterSelectMenu(GeneralMenu):
    def __init__(self,game,difficulty=None):
        super().__init__(game)
        self.image_name = "character_select_background.png"
        self.image_path = os.path.join(str(self.screens_path),self.image_name)
        self.background = pygame.image.load(self.image_path)
        self.p1_choice = None
        self.p2_choice = None
        self.difficulty = difficulty
    
        self.player_1_swordsman_opt = pygame.Rect(168,31,166,139)
        self.player_2_swordsman_opt = pygame.Rect(951,31,166,139)
        
    def render(self):
        self.game.screen.blit(self.background,(0,0))
        pygame.display.flip()
        
    def check_menu_transition(self,event):
        # retrieves current mouse pos as tuple(x,y)
        cur_mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            # checks if option clicked, if so initialise new menu and push
            if self.check_opt_press(cur_mouse_pos,self.player_1_swordsman_opt) and self.p1_choice == None:
                self.p1_choice = "Swordsman"
                    
            if self.check_opt_press(cur_mouse_pos,self.player_2_swordsman_opt) and self.p2_choice == None:
                self.p2_choice = "Swordsman"
         
        # checks if both players have chosen a character 
        if self.p1_choice and self.p2_choice != None:
            if self.difficulty != None:
                game_loop = AIGameLoop(self.p1_choice,self.p2_choice,self.game,self.difficulty)
            # initialise game loop object
            else:
                game_loop = GameLoop(self.p1_choice,self.p2_choice,self.game)
            # resets options after game initialised
            self.p1_choice = None  
            self.p2_choice = None
            # push onto the stack
            self.game.menu_stack.push(game_loop)
            
            
class OnlineCharacterSelectMenu(GeneralMenu):
    def __init__(self,game,player_num,lobby_client,lobby_id):
        super().__init__(game)
        self.image_name = "character_select_background.png"
        self.image_path = os.path.join(str(self.screens_path),self.image_name)
        self.background = pygame.image.load(self.image_path)
        self.player_num = player_num
        self.lobby_client = lobby_client
        self.lobby_id = lobby_id
        self.chosen = False
        self.started = False
        self.disconnected = False
        
        
       
        
    
        if self.player_num == 1:
            self.swordsman_opt = pygame.Rect(168,31,166,139)
        else:
            self.swordsman_opt = pygame.Rect(951,31,166,139)
            
    # override parent function so that client disconnects when exiting the menu
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # disconnects 2 menus back
                    self.lobby_client.close_connection()
                    self.game.menu_stack.pop_off(2)
                    
            self.check_menu_transition(event)
            self.check_if_enemy_left()
            
    def render(self):
        self.game.screen.blit(self.background,(0,0))
        self.lobby_client.check_lobby_update()
        pygame.display.flip()
        
    def check_menu_transition(self,event):
        cur_mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            if self.check_opt_press(cur_mouse_pos,self.swordsman_opt) and not self.chosen:
                response = self.lobby_client.send_character("Swordsman",str(self.lobby_id),str(self.player_num))
                if response == "character received":
                    self.chosen = True
          
        self.check_game_start()
        
    
    def check_game_start(self):
        
        lobby_data = self.lobby_client.get_lobby_data()
        if "player 1"  in lobby_data[self.lobby_id] and "player 2" in lobby_data[self.lobby_id] and self.started == False:
            self.started = True
            p1_choice = lobby_data[self.lobby_id]["player 1"]
            p2_choice = lobby_data[self.lobby_id]["player 2"]
            online_game = OnlineGameLoop(p1_choice,p2_choice,self.game,self.player_num,self.lobby_id,self.lobby_client)
            self.game.menu_stack.push(online_game)
  
    def check_if_enemy_left(self):
        if self.lobby_client.check_game_empty(self.lobby_id) == True and not self.disconnected:
            self.disconnected = True
            self.lobby_client.close_connection()
            self.game.menu_stack.pop_off(2)
        
