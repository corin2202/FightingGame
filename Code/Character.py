import pygame
import os

class Character:
    def __init__(self,player_num,x_coord,y_coord):
        self.player_num = player_num
        
    
        if player_num == 1:
            self.run_key = pygame.K_d
            self.walk_key = pygame.K_a
            self.jump_key = pygame.K_w
            self.light_swing_key = pygame.K_f
            self.heavy_swing_key = pygame.K_g
            self.block_key = pygame.K_LSHIFT
            self.down_key = pygame.K_s
            
        if player_num == 2:
            self.run_key = pygame.K_RIGHT
            self.walk_key = pygame.K_LEFT
            self.jump_key = pygame.K_UP
            self.light_swing_key = pygame.K_SEMICOLON
            self.heavy_swing_key = pygame.K_l  # L,,
            self.block_key = pygame.K_RCTRL
            self.down_key = pygame.K_DOWN
            
        
            
        
        
        
            
            
   
        self.y_gravity = 1
        self.y_velocity = 0
        self.in_air = False

        self.run_speed = 12
        self.walk_speed = 5
        
        # states
        self.walking = False
        self.running = False
        self.jumping = False
        self.blocking = False
        self.stunned = False
        
        
        self.attack_type = ""
        self.attacking = False
        self.hurtbox_drawn = True
        self.is_hit = False
        self.hit_type = ""
        
        self.block_cd = 900
        self.heavy_cd = 1000
        self.light_cd = 500
        
        self.last_block = 0
        self.last_light = 0
        self.last_heavy = 0
        
        self.light_dmg = 5
        self.heavy_dmg = 10
        
        # animation variables
        self.all_animations = {}
        self.last_frame = 0
        
        self.current_frame = 0
        
        self.hitbox = pygame.Rect((x_coord,y_coord,90,220))
        
        if player_num == 1:
            self.flip = False
        else:
            self.flip = True
            
        self.hp= 100
        self.bp = 0
        
    # Draws the hitbox at x and y coords    
    def draw(self,surface):
        pygame.draw.rect(surface,(255,0,0),self.hitbox)
        
    # Function that returns the relative path to the fighter/swordsman character sprites
    def path_to_sprites(self,char_name):
        cur_dir = os.getcwd()
        # stores the parent directory to the current working directory
        parent_dir = os.path.dirname(cur_dir)
        # creates a new path to the sprites directory, either Fighter_Sprites or Swordsman_Sprites
        character_sprites_path = os.path.join(str(parent_dir),"Character_Sprites\{character}_Sprites".format(character = char_name))
        return character_sprites_path
    
    # loads the needed animations into the dictionary, key= state, value = list of sprite objects   
    def load_animations(self,char_name):
        all_states = ["idle","walk","run","jump","n_light","n_heavy","s_light","g_block","a_block","d_light","hit_heavy","hit_light","stun"]
        for state in all_states:
            # creates a key for state with an empty list
            self.all_animations[state] = []
            # stores the path to the Swordsman_Sprites directory
            char_sprites_path = self.path_to_sprites(char_name)
            # Creates the path to the current state e.g Swordsman_Sprites\S_idle
            state_path = os.path.join(str(char_sprites_path),char_name[0]+"_{}".format(state))
            # returns list of strings for each name of the image in the directory
            images_list = os.listdir(state_path)
            
            # loops through image names
            for img in images_list:
                # creates path to the current image name
                img_path = os.path.join(str(state_path),"{}".format(img))
                # stores the image file
                img_object = pygame.image.load(img_path)
                # adds the image to the list of the corresponding state
                self.all_animations[state].append(img_object)
                
    
        
        
        
        
    def run(self,screen_width):
        self.running = True
        # decreases x if flipped and increases x if not flipped
        self.hitbox.x -= self.run_speed * (-1 if not self.flip else 1)
        # clamps the x value within the range 0 to screenwidth - hitbox width
        self.hitbox.x = max(0, min(self.hitbox.x, screen_width - self.hitbox.width)) 
   
            
            
    def walk(self,screen_width):
        self.walking = True
        # increases the x coordinate if flipped and decreases the x coordinate if not flipped
        self.hitbox.x += self.walk_speed * (-1 if not self.flip else 1)
        # clamps the x value within the range 0 to screenwidth - hitbox width
        self.hitbox.x = max(0, min(self.hitbox.x, screen_width - self.hitbox.width))
    

            
    def jump(self):
        # only performs jump if on the ground
        if self.jumping == False:
            self.jumping = True
            # adds the y veloicty for the jump to the variable
            self.y_velocity += 25
            self.in_air = True
        
            
    def apply_gravity(self,screen_height):
        if self.in_air == True:
            # checks if the next position of the hitbox does not exceed floor boundary
            if self.hitbox.bottom - self.y_velocity <= screen_height-70:
                # takes away the y velocity from the hitbox y coord (pos y_vel goes up, neg y_vel goes down)
                self.hitbox.y -= self.y_velocity
                # reduces the y vel by the gravity amount to create accel and deccel
                self.y_velocity -= self.y_gravity   
            else:
                # if the next position of hitbox exceeds boundary, at floor so reset values
                self.in_air = False
                self.jumping = False
                self.y_velocity = 0
                self.hitbox.bottom = screen_height-70
                
        
    def set_attack(self,attack):
        self.attack_type = attack
        self.attacking = True
        self.hurtbox_drawn = False
        
        
    def check_flip(self,enemy):
        # Checks if enemy is on the opposite side, if so sets turn_around to False/True
        if enemy.char.hitbox.midtop[0] > self.hitbox.midtop[0]:
            self.flip = False
        else:
            self.flip = True
            
        if self.player_num == 1:
            
            if not self.flip:
                self.run_key = pygame.K_d
                self.walk_key = pygame.K_a
            else:
                self.run_key = pygame.K_a
                self.walk_key = pygame.K_d
                
        else:
            
            if not self.flip:
                self.run_key = pygame.K_RIGHT
                self.walk_key = pygame.K_LEFT
            else:
                self.run_key = pygame.K_LEFT
                self.walk_key = pygame.K_RIGHT
            
            
    def reset_frame(self):
        self.current_frame = 0
        
    def terminate_attack(self,attack):
        if self.current_frame == len(self.all_animations[attack])-1:
            self.attacking = False
        
    def terminate_hit(self,hit_type):
        if self.current_frame == len(self.all_animations[hit_type])-1:
            self.is_hit = False
            
    def terminate_stun(self):
        if self.current_frame == len(self.all_animations["stun"])-1:
            self.stunned = False
            
    def stun_check(self):
        if self.bp >= 20:
            self.bp = 0
            self.stunned = True
            self.blocking = False
            self.reset_frame()
                

       
        
        
        