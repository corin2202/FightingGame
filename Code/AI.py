import random
import pygame
from Swordsman import Swordsman

class SwordsmanAI(Swordsman):
    def __init__(self,player_num,x_coord,y_coord,difficulty):
        super().__init__(player_num,x_coord,y_coord)
        
        self.start_run_timer = 0
        self.backing_off_timer = 0
        self.block_timer = 0
        self.block_duration = 0
        self.in_fighting_range = False
        self.backing_off = False
        self.safe = False
        self.jump_overL = False
        self.jump_overR = False
        self.aggressive = True
        # increased odds for moves if difficulty is hard
        self.mode_mult = 2 if difficulty == "hard" else 1
        
        
    def update(self,game,enemy):
        
        current_time = pygame.time.get_ticks()
        # call continuous movement functions
        # only allows movement while not attacking, attacking freezes mid air
        self.walking = False
        self.running = False
        
        self.handle_gravity(game.screen.get_height())
        
        
        self.perform_move(game,enemy,current_time)
        
        
    def check_state(self):
        if self.hp < 30:
            self.aggressive = False
        else:
            self.aggressive = True
                
                
        
    def perform_move(self,game,enemy,current_time):
        
        # gets the dictionary of the enemy states and coordinates
        enemy_states = enemy.get_states()
        
        # checks if the player is within fighting range
        self.check_state()
        self.range_check(enemy_states["x"],game.screen.get_width(),current_time)
        self.handle_move(enemy_states["attacking"],enemy_states["blocking"],enemy_states["attack_type"],current_time,game.screen.get_width())
        self.handle_jump_over(enemy_states["x"],game.screen.get_width())
        
    def range_check(self,enemy_x,screen_width,current_time):
      
        
        # checks if the gap between them is classed as fighting range or not
        # also checks for the secondary safety gap used for backing off , larger than the fighting range
        if self.flip:
            if self.hitbox.x- enemy_x > 270:
                self.in_fighting_range = False
                if self.hitbox.x - enemy_x > 400:
                    self.safe = True
                else:
                    self.safe = False
                    
            elif self.hitbox.x - enemy_x <= 270:
                self.in_fighting_range = True
                
        # opposite for when character flipped        
        else:
            if enemy_x - self.hitbox.x > 270:
                self.in_fighting_range = False
                if enemy_x - self.hitbox.x > 400:
                    self.safe = True
                else:
                    self.safe = False
                    
            elif enemy_x - self.hitbox.x <= 250:
                self.in_fighting_range = True
            
                
                
    def handle_move(self,enemy_attacking,enemy_blocking,enemy_attack_type,current_time,screen_width):
        # if gap between too large, runs after a delay
        # the timer resets after it is within range
        if not self.in_fighting_range:
            if self.aggressive:
                self.chase_enemy(screen_width)
            
        else:
            # stop chasing when within range
            self.start_run_timer = 0
            # calculates move when in range
            self.calculate_fighting_move(enemy_attacking,enemy_blocking,enemy_attack_type,current_time,screen_width)
        
        # walks backwards to safety when low hp (not aggressive)
        if not self.aggressive:
            self.handle_back_off(screen_width)
                       
            
    def chase_enemy(self,screen_width):
        # if gap between too large, runs after a delay
        # the timer resets after it is within range
        if self.start_run_timer == 25:
            self.handle_run(screen_width)
        else:
            self.start_run_timer += 1
    
    
    def calculate_fighting_move(self,enemy_attacking,enemy_blocking,enemy_attack_type,current_time,screen_width):
        # decides whether to block or jump back when attack thrown
        if enemy_attacking:
            self.handle_enemy_attack_logic(enemy_attack_type,screen_width,current_time)
        else:
            # performs light/heavy on the enemy while blocking
            if enemy_blocking:
                self.handle_enemy_block(current_time)
            else:
                # performs neutral or side light when in fighting range
                self.handle_light_logic(screen_width,current_time)
                # stops the block once the enemy finishes attacking and duration has been met
                self.handle_block_termination()
                
                
    def handle_enemy_attack_logic(self,enemy_attack_type,screen_width,current_time):
        chance = random.random()
        
        if enemy_attack_type[-5:] == "heavy":
            if chance < 0.06 * self.mode_mult:
                self.handle_walk(screen_width)
                self.handle_jump()
              
            
        elif enemy_attack_type[-5:] == "light":
            # start the block for a random duration
            if chance < 0.02*self.mode_mult:
                if not self.blocking:
                    self.block_duration = random.randint(20,50)
                    self.handle_block_start(current_time)
                
                
    def handle_block_termination(self):
        # continues block for duration or stops it and resets
        if self.blocking:
            if self.block_timer < self.block_duration:
                self.block_timer +=1
            else:
                self.handle_block_stop()
                self.block_timer = 0
                
            
            
            
            
            
        
                        
    def handle_light_logic(self,screen_width,current_time):
        # generate a random number between 0-1
        chance = random.random()
                
        # chance for a light attack
        if chance < 0.03 * self.mode_mult and not self.in_air:
            chance = random.random()
                    
            # 50\50 chance to perform a side or a neutral light
            if chance > 0.5* self.mode_mult:
                self.handle_ground_light(current_time)
            else:
                self.handle_run(screen_width)
                self.handle_ground_light(current_time)
                        
    def handle_enemy_block(self,current_time):
        # generates random chance of performing a heavy when blocking or a light 
        chance = random.random()
        if chance < 0.005 * self.mode_mult:
            self.handle_heavy(current_time)
        elif chance < 0.03* self.mode_mult:
            self.handle_ground_light(current_time)
                        
                        
    def handle_back_off(self,screen_width):
        # if not safe then roll a chance to start backing off
        if self.backing_off == False and not self.safe:
            chance = random.random()
            if chance < 0.05* self.mode_mult:
                self.backing_off = True
                self.back_off_timer = 0
                
        else:
            # reset the backing off timer, finished backing off
            if self.back_off_timer == 40:
                self.backing_off = False
            else:
                # backs off as long as the timer is less than 40
                self.back_off_timer += 1
                self.handle_walk(screen_width)
                
                
    def check_jump_condition(self,enemy_x):
        if self.hitbox.x >= 1280 - self.hitbox.width and self.in_fighting_range:
            self.jump_overR = True
        elif self.hitbox.x <= 0 and self.in_fighting_range:
            self.jump_overL = True
            
            
                
    def handle_jump_over(self,enemy_x,screen_width):
        
        # checks which side of map AI is hitting
        self.check_jump_condition(enemy_x)
        
        # if at  right side of map
        if self.jump_overR:
        
            if self.hitbox.x > enemy_x - 100:
                # perform the run and jump until character flipped
                if self.hitbox.x - enemy_x >= 0:
                    self.handle_jump()
                    self.handle_run(screen_width)
                else:
                    # once flipped walk backwards for a bit until 100 pixels past the player enemy
                    self.handle_walk(screen_width)
            else:
                # reset condition once finished
                self.jump_overR = False
                
        # same as previous block except for left side of the map, run and jump then walk until 100 pixels ahead of player        
        if self.jump_overL:
            if enemy_x + 100 > self.hitbox.x:
                if enemy_x - self.hitbox.x >= 0:
                    self.handle_jump()
                    self.handle_run(screen_width)
                else:
                    self.handle_walk(screen_width)
            else:
                self.jump_overL = False



    

        
        
       

                
       
            

       