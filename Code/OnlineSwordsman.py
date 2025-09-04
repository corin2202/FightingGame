import pygame
import socket

from Swordsman import Swordsman


class OnlineSwordsman(Swordsman):
    def __init__(self,player_num,x_coord,y_coord,client_socket,serv_address):
        super().__init__(player_num,x_coord,y_coord)
        self.game_socket = client_socket
        self.server_address = serv_address
        
    # FOR ONLINE MODE
    def update_movement(self,states):
        
        # sets the states of the remote player to the states received
        # walking/running handling not needed, just sets coordinates
        self.hitbox.x = states["x"]
        self.hitbox.y = states["y"]
        self.running = states["running"]
        self.walking = states["walking"]
        self.in_air = states["in_air"]
        #self.hp = states["hp"]
        #self.bp = states["bp"]
        
        # checks if a jump is starting, if so reset frame like in the handle jump function
        if states["jumping"] == True and self.jumping == False:
            self.reset_frame()
            
        self.jumping = states["jumping"]
        
        # if an attack is to be performed and not currently performing one
        if states["attacking"] == True and self.attacking == False:
            current_time = pygame.time.get_ticks()
            
            if states["attack_type"] == "n_light" or states["attack_type"] == "s_light":
                self.handle_ground_light(current_time)
                
            if states["attack_type"] == "n_heavy":
                self.handle_heavy(current_time)
                
            if states["attack_type"] == "d_light":
                self.handle_air_light(current_time)
                
        if states["blocking"] == True and not self.blocking:
            current_time = pygame.time.get_ticks()
            self.handle_block_start(current_time)
          
        if states["blocking"] == False and self.blocking:
            self.handle_block_stop()
      
        
        
    
        
    
