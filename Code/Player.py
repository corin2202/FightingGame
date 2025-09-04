import pygame
import socket
import json


from Swordsman import Swordsman
from OnlineSwordsman import OnlineSwordsman
from AI import SwordsmanAI


class Player:
    def __init__(self,player_number,character_selected,ai_mode,online,difficulty=None,client_sock=None,serv_address = None):
        self.player_number = player_number
        self.character_selected = character_selected
        self.score = 0
        self.ai_mode = ai_mode
        self.online = online
        self.client_socket = client_sock
        self.server_address = serv_address

        
        if self.character_selected == "Swordsman":
            if player_number == 1:
                if not self.online:
                    # initialise character
                    self.char = Swordsman(1,200,430)
                    # load animations
                    self.char.load_animations("Swordsman")
                else:
                    self.char = OnlineSwordsman(1,200,430,client_sock,serv_address)
                    self.char.load_animations("Swordsman")
             
                
            if player_number == 2:
                if not self.ai_mode:
                    if not self.online:
                        self.char = Swordsman(2,700,430)
                        self.char.load_animations("Swordsman")
                    else:
                        self.char = OnlineSwordsman(2,700,430,client_sock,serv_address)
                        self.char.load_animations("Swordsman")
                else:
                    self.char = SwordsmanAI(2,700,430,difficulty)
                    self.char.load_animations("Swordsman")
                  
                
                
                
    def reset(self):
        self.set_hp(100)
        self.set_bp(0)
        self.reset_dmg()
        
        if self.player_number == 1:
            self.set_coords(200,430)
        else:
            self.set_coords(700,430)
            
            
    def get_states(self):
        states = {"attacking":self.char.attacking,
                     "walking":self.char.walking,
                     "running":self.char.running,
                     "attack_type":self.char.attack_type,
                     "blocking":self.char.blocking,
                     "jumping":self.char.jumping,
                     "hit":self.char.is_hit,
                     "stunned":self.char.stunned,
                      "x":self.char.hitbox.x,
                      "y":self.char.hitbox.y,
                      "player_num":self.char.player_num,
                      "in_air":self.char.in_air
                      #"hp":self.char.hp,
                      #"bp":self.char.bp
        }
        
        return states
            
     
    def send_client_data(self):
        states = self.get_states()
        serialised_states = json.dumps(states)
        self.client_socket.sendto(serialised_states.encode("utf-8"), self.server_address)
                
    def get_hp(self):
        return self.char.hp
    
    def set_hp(self,newhp):
        self.char.hp = newhp
    
    def get_bp(self):
        return self.char.bp
    
    def set_bp(self,newbp):
        self.char.bp = newbp
        
        
    
    def set_coords(self,x,y):
        self.char.hitbox.x = x
        self.char.hitbox.y = y
        
    def sudden_death_damage(self):
        self.char.light_dmg *= 2
        self.char.heavy_dmg *= 2
        
    def reset_dmg(self):
        self.char.light_dmg = 5
        self.char.heavy_dmg = 10
        
        
        
            
            
        
        

        
        
