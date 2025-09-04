import pygame
import os



from Player import Player
from HUD import HUD

from UDPclient import GameClient


class GameLoop:
    def __init__(self,p1_choice,p2_choice,game):
        
        pygame.init()
        
        self.game = game
        self.winner = None
        self.current_round = 1
        self.rounds_to_win = 3
        self.game_state = "round 1"
        
        
        # initialise players here
        self.player_1 = Player(1,p1_choice,False,False)  # not ai, not online
        self.player_2 = Player(2,p2_choice,False,False)
        
        # initialise HUD with reference to players
        self.game_HUD = HUD(self.player_1,self.player_2)
        
        self.font = pygame.font.Font(None, 120)
        
        # Creates a clock to set the FPS
        self.clock = pygame.time.Clock()
        self.GAME_FPS = 60
        
        # Fetch background
        self.cur_dir = os.getcwd()
        # stores the parent directory to the current working directory
        self.parent_dir = os.path.dirname(self.cur_dir)
        # creates a new path to the screens directory, this works for all file structures for any machine
        self.screens_path = os.path.join(str(self.parent_dir),"Screens")
        
        self.image_name = "raft_background.png"
        self.image_path = os.path.join(str(self.screens_path),self.image_name)
        # loads the image to a variable to be displayed
        self.background = pygame.image.load(self.image_path)
        
    def check_for_new_round(self):
        if self.player_1.get_hp() <= 0:
            self.player_2.score += 1

            if self.player_2.score == self.rounds_to_win:
                self.winner = "2"
           

            else:
                self.current_round += 1
                self.reset_round()

        elif self.player_2.get_hp() <= 0:
            self.player_1.score += 1

            if self.player_1.score == self.rounds_to_win:
                self.winner = "1"
        
 
            else:
                self.current_round += 1
                self.reset_round()
                
    def reset_round(self):
        # Reset relevant variables for a new round
        self.player_1.reset()  
        self.player_2.reset()
        
    
        
        # reset timer aswell
        self.game_HUD.reset()
 
        self.game_state = "round {}".format(self.current_round)
       
    def display_message(self, round_text):
        text = self.font.render(round_text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.game.screen.get_width() // 2, self.game.screen.get_height() // 2 - 200))
        self.game.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)  # Display for 2 seconds
        
        
    def manage_round(self):
        
        # if the game state is between rounds
        if self.game_state != "playing":
            # if at round 1 display the background so the text isnt on the previous character select screen
            if self.game_state == "round 1":
                self.game.screen.blit(self.background,(0,0))
                
            # display the current round message and set the game state to playing after a time delay
            if self.winner == None:    
                self.display_message("ROUND {}".format(self.current_round))
                self.game_state = "playing"
            # if a winner is detected, set the game message to read winner and end the game
            else:
                self.display_message("PLAYER "+self.winner+" WINS")
                
                self.game_state = "end"
                # returns to character select screen
                self.game.menu_stack.pop_off()
                     
    def handle_input(self):
        
        # checks for dead players & winners
        self.check_for_new_round()
        
        # if game in playing state call the game loop functions
        if self.game_state == "playing":
            keys = pygame.key.get_pressed()
            events = pygame.event.get()
        
            # call input functions for both
            self.player_1.char.handle_input(self.game,events,keys)
            self.player_2.char.handle_input(self.game,events,keys)
        
            # check if players flip
            self.player_1.char.check_flip(self.player_2)
            self.player_2.char.check_flip(self.player_1)
        
        
            # player animation updates
            self.player_1.char.update_player_animation(self.player_2)
            self.player_2.char.update_player_animation(self.player_1)
      
    def render(self):
        
        # renders the round messages & winner messages & exits game if won
        self.manage_round()
        
        self.clock.tick(self.GAME_FPS)
        # render background
        
        # calls the necessary render functions for the game loop
        if self.game_state == "playing":
            # first renders background
            self.game.screen.blit(self.background,(0,0))
        
            #self.player_1.char.draw(self.game.screen)   # hitbox
            #self.player_2.char.draw(self.game.screen)
        
            # render players, 2 will appear to be above player 1
            self.player_1.char.display_character(self.game.screen)
            self.player_2.char.display_character(self.game.screen)
        
            # render HUD on top
            self.game_HUD.render(self.game.screen)
        
        
        
        pygame.display.flip()
        
        
        
        
        
        
        
class AIGameLoop(GameLoop):
    def __init__(self,p1_choice,p2_choice,game,difficulty):
        super().__init__(p1_choice,p2_choice,game)
        
        # initialise players here
        self.player_1 = Player(1,p1_choice,False,False) # not ai , not online
        self.player_2 = Player(2,p2_choice,True,False,difficulty)  # is ai, not online
        self.game_HUD = HUD(self.player_1,self.player_2)
        
        
    def handle_input(self):
        # checks for dead players & winners
        self.check_for_new_round()
        
        # if game in playing state call the game loop functions
        if self.game_state == "playing":
            keys = pygame.key.get_pressed()
            events = pygame.event.get()
        
            # call input functions for both
            self.player_1.char.handle_input(self.game,events,keys)
            #self.AIplayer_2.char.draw(self.game.screen)
            self.player_2.char.update(self.game,self.player_1)
        
            # check if players flip
            self.player_1.char.check_flip(self.player_2)
            self.player_2.char.check_flip(self.player_1)
            
            #print(self.AIplayer_2.char.hitbox.x)
        
            # player animation updates
            self.player_1.char.update_player_animation(self.player_2)
            self.player_2.char.update_player_animation(self.player_1)
            
            
    def render(self):
        
        # renders the round messages & winner messages & exits game if won
        self.manage_round()
        
        self.clock.tick(self.GAME_FPS)
        # render background
        
        # calls the necessary render functions for the game loop
        if self.game_state == "playing":
            # first renders background
            self.game.screen.blit(self.background,(0,0))
        
            #self.player_1.char.draw(self.game.screen)   # hitbox
            #self.player_2.char.draw(self.game.screen)
        
            # render players, 2 will appear to be above player 1
            self.player_1.char.display_character(self.game.screen)
            self.player_2.char.display_character(self.game.screen)
        
            # render HUD on top
            self.game_HUD.render(self.game.screen)
            
     
        
        
        
        pygame.display.flip()
        
        
    def check_for_new_round(self):
        if self.player_1.get_hp() <= 0:
            self.player_2.score += 1
            self.player_1.char.stats.increment_stat("Deaths")

            if self.player_2.score == self.rounds_to_win:
                self.winner = "2"
                self.player_1.char.stats.increment_stat("Losses")
                self.player_1.char.stats.increment_stat("Games Played")
           
            else:
                self.current_round += 1
                self.reset_round()

        elif self.player_2.get_hp() <= 0:
            self.player_1.score += 1
            self.player_1.char.stats.increment_stat("Kills")

            if self.player_1.score == self.rounds_to_win:
                self.winner = "1"
                self.player_1.char.stats.increment_stat("Wins")
                self.player_1.char.stats.increment_stat("Games Played")
        
 
            else:
                self.current_round += 1
                self.reset_round()
        
        
        
        
        
        
        
        
        
        
class OnlineGameLoop(GameLoop):
    def __init__(self,p1_choice,p2_choice,game,player_num,lobby_id,lobby_client):
        
        
        
        super().__init__(p1_choice,p2_choice,game)
        
        
        self.local_player_num = player_num
        self.lobby_id = lobby_id
        self.lobby_client = lobby_client

        # Initialize the game client for both players
        self.game_client = GameClient(player_num,p1_choice,p2_choice,lobby_id,self.game)
        self.game_client.start()
        
        self.local_player = self.game_client.local_player
        self.remote_player = self.game_client.remote_player
        
        self.disconnected = False
       
            

        
        # Initialize HUD with a reference to players
        if self.local_player_num == 1:
            self.game_HUD = HUD(self.local_player, self.remote_player)
        else:
            self.game_HUD = HUD(self.remote_player, self.local_player)
        
            
            
    def check_for_new_round(self):
        if self.local_player.get_hp() <= 0:
            self.remote_player.score += 1
            self.local_player.char.stats.increment_stat("Deaths")
            
            if self.remote_player.score == self.rounds_to_win:
                self.winner = str(self.remote_player.player_number)
                self.local_player.char.stats.increment_stat("Losses")
                self.local_player.char.stats.increment_stat("Games Played")
           
            else:
                self.current_round += 1
                self.reset_round()

        elif self.remote_player.get_hp() <= 0:
            self.local_player.score += 1
            self.local_player.char.stats.increment_stat("Kills")

            if self.local_player.score == self.rounds_to_win:
                self.winner = str(self.local_player.player_number)
                self.local_player.char.stats.increment_stat("Wins")
                self.local_player.char.stats.increment_stat("Games Played")

            else:
                self.current_round += 1
                self.reset_round()
                
                

                
                


                
    def reset_round(self):
        # Reset relevant variables for a new round
        self.local_player.reset()  
        self.remote_player.reset()
        
    
        
        # reset timer aswell
        self.game_HUD.reset()
        #self.game_state = "playing"
        self.game_state = "round {}".format(self.current_round)
                
                
    def handle_input(self):
        
        # checks for dead players & winners
        self.check_for_new_round()
        
        # if game in playing state call the game loop functions
        if self.game_state == "playing":
            keys = pygame.key.get_pressed()
            events = pygame.event.get()
            
        
            # call input functions for local player
            self.local_player.char.handle_input(self.game,events,keys)
            self.local_player.send_client_data()   
        
            # check if players flip
            self.local_player.char.check_flip(self.remote_player)
            self.remote_player.char.check_flip(self.local_player)
        
        
            # player animation updates
            self.local_player.char.update_player_animation(self.remote_player)
            self.remote_player.char.update_player_animation(self.local_player)
            
            # checks for lobby data if other player has left if so then game disconnects
            self.lobby_client.check_lobby_update(2000)
            self.disconnect_if_empty()
            
            # if quit midgame, then disconnects lobby client
            for event in events:
                if event.type == pygame.QUIT:
                    self.lobby_client.close_connection()
            
            
    def disconnect_if_empty(self):
        if self.lobby_client.check_game_empty(self.lobby_id) == True and self.disconnected == False:
            self.disconnected = True
            self.lobby_client.close_connection()
            self.game.menu_stack.pop_off(3)
                
            
    def render(self):
        # renders the round messages & winner messages & exits game if won
        self.manage_round()
        
        self.clock.tick(self.GAME_FPS)
        # render background
        
        # calls the necessary render functions for the game loop
        if self.game_state == "playing":
            # first renders background
            self.game.screen.blit(self.background,(0,0))
        
    
            # render players, remote will appear to be above local
            self.local_player.char.display_character(self.game.screen)
            self.remote_player.char.display_character(self.game.screen)
        
            # render HUD on top
            self.game_HUD.render(self.game.screen)
        
        
        
        pygame.display.flip()
                
                
            
            

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        