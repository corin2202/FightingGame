from Character import Character

from StatTable import HashTable

import pygame
import os

class Swordsman(Character):
    def __init__(self,player_num,x_coord,y_coord):
        
        super().__init__(player_num,x_coord,y_coord)
        idle_sprite_path = os.path.join(str(self.path_to_sprites("Swordsman")),"S_idle","S_idle1.png")
        # sets first sprite to the first idle image
        self.cur_sprite = pygame.image.load(idle_sprite_path)
        
        self.stats = HashTable()
        
        # sprite offsets for each set of animations
        self.offsets = {"idle":(-55,-50),
                                "walk":(-80,-80),
                                "run":(-170,-20),
                                "jump":(-145,-50),
                                "n_light":(-100,-120),
                                "n_heavy":(-70,-130),
                                "s_light":(-70,-90),
                                "g_block":(-50,-60),
                                "a_block":(-60,-80),
                                "d_light":(-70,-90),
                                "hit_light":(-45,-90),
                                "hit_heavy":(-70,10),
                                "stun":(-55,-50)
    }
        
        # current offset to be used when drawing
        self.current_offset = self.offsets["idle"]
        
    def play_animation(self, cur_state, continuous=True,animation_cd = 150):
        current_time = pygame.time.get_ticks()
        
        # resets back to beginning when last frame reached
        if continuous:
            self.current_frame = self.current_frame % len(self.all_animations[cur_state])
        
        # sets current sprite to one associated with current frame and resizes it
        self.cur_sprite = self.all_animations[cur_state][self.current_frame]
        self.cur_sprite = pygame.transform.scale(self.cur_sprite, (int(self.cur_sprite.get_width() * 1.9), int(self.cur_sprite.get_height() * 1.9)))
        # applies the offset
        self.current_offset = self.offsets[cur_state]
        
        # if enough time passed between frames, increment the frame
        if current_time - self.last_frame >= animation_cd:
            self.current_frame += 1
            # pause at the last frame
            if not continuous and self.current_frame == len(self.all_animations[cur_state]):
                self.current_frame -= 1
            self.last_frame = current_time
    
                    
                
      
            
    def draw_hurtbox(self,enemy):
        # frame 2 is the image where hitboxes need to be drawn
        if self.current_frame == 2 and not self.hurtbox_drawn:
            self.hurtbox_drawn = True
            # corresponding hitbox sizes depend on the type of attack
            if self.attack_type == "n_light":
                hurtbox = pygame.Rect(self.hitbox.midtop[0]+self.flip*-230,self.hitbox.y-10,240,40)
            elif self.attack_type == "n_heavy":
                hurtbox = pygame.Rect(self.hitbox.left+self.flip*-250,self.hitbox.y-20,345,220)
            elif self.attack_type == "s_light":
                hurtbox = pygame.Rect(self.hitbox.midtop[0]+self.flip*-230,self.hitbox.y-85,240,200)
            elif self.attack_type == "d_light":
                hurtbox = pygame.Rect(self.hitbox.x+self.flip*-100,self.hitbox.y-85,250,380)
            
            # performs hit detection after hitbox drawn
            self.detect_hit(enemy,hurtbox)
            
            
    def detect_hit(self, enemy, hurtbox):
        # if hurtbox hits enemies hitbox, health taken away or block meter
        if hurtbox.colliderect(enemy.char.hitbox):
            self.handle_hit(enemy)

    def handle_hit(self, enemy):
        if not enemy.char.blocking:
            self.handle_non_blocking_hit(enemy)
        else:
            self.handle_blocking_hit(enemy)

    def handle_non_blocking_hit(self, enemy):
        # play animation and inflict damage if not stunned, if stunned just inflict damage
        if not enemy.char.stunned:
            self.process_hit_animation(enemy)
            self.inflict_damage(enemy)
        else:
            self.inflict_damage(enemy)

    def process_hit_animation(self, enemy):
        enemy.char.is_hit = True
        # sets enemy hit type to either light or heavy (5 letters long each)
        enemy.char.hit_type = "hit_{}".format(self.attack_type[-5:])
        enemy.char.reset_frame()

    def inflict_damage(self, enemy):
        # light attacks to small damage
        # heavy attacks do more damage
        enemy_hp = enemy.get_hp()
        if "light" in self.attack_type:
            damage = self.light_dmg
        else:
            damage = self.heavy_dmg
            
        enemy.set_hp(enemy_hp - damage)
        self.stats.increment_stat("Damage",damage)

    def handle_blocking_hit(self, enemy):
        if "light" in self.attack_type:
            self.process_blocking_light_hit(enemy)
        elif "heavy" in self.attack_type:
            self.process_blocking_heavy_hit(enemy)

    def process_blocking_light_hit(self, enemy):
        enemy_bp = enemy.get_bp()
        enemy.set_bp(enemy_bp + self.light_dmg)
        enemy.char.stun_check()

    def process_blocking_heavy_hit(self, enemy):
        # heavy attack on a block will instantly fill meter and stun the enemy
        enemy.set_bp(50)
        enemy.char.stun_check()  
                
    # function that deals with the animation hierarchy
    # stun has most priority and attacks & movement have the lowest
    def update_player_animation(self,enemy):
        if not self.stunned:
            if not self.is_hit:
                if not self.attacking:
                    self.update_non_attack_animations()
                else:
                    self.update_attack_animation(enemy)
            else:
                self.update_hit_animation()
        else:
            self.update_stun_animation()

    def update_non_attack_animations(self):
        # always performs jump animation unless air blocking
        if not self.jumping:
            if self.walking:
                self.play_animation("walk")
            elif self.running:
                self.play_animation("run")
            elif self.blocking:
                self.play_animation("g_block", False)
            else:
                self.play_animation("idle")
        else:
            if self.blocking:
                self.play_animation("a_block", False)
            else:
                self.play_animation("jump", False)

    def update_attack_animation(self,enemy):
        # performs the animation once
        self.play_animation(self.attack_type, False)
        # draws the hitbox on the correct frame
        self.draw_hurtbox(enemy)
        # stops animation when the attack reaches the end
        self.terminate_attack(self.attack_type)

    def update_hit_animation(self):
        self.play_animation(self.hit_type, False, 400) # cooldown is 400ms
        self.terminate_hit(self.hit_type)

    def update_stun_animation(self):
        self.play_animation("stun", False, 500)  # cooldown is 500ms
        self.terminate_stun()
        
        
    def handle_input(self,game,events,keys):
        # retrieves time since start of execution
        current_time = pygame.time.get_ticks()
        
        # as walking and running is continuous, must be reset each frame
        self.walking = False
        self.running = False
        
        # if held down again, changed to be true and walk/run performed
        if keys[self.walk_key]:
            self.handle_walk(game.screen.get_width())
        if keys[self.run_key]:
            self.handle_run(game.screen.get_width())
            
        # calls apply_gravity has internal conditions for applying it   
        self.handle_gravity(game.screen.get_height())
        
        for event in events:
            # KEYDOWN EVENTS
            if event.type == pygame.KEYDOWN:
                # JUMP
                if event.key == self.jump_key:
                    self.handle_jump()
                
                # DOWN LIGHT
                if keys[self.down_key]:
                    if event.key == self.light_swing_key:
                        self.handle_air_light(current_time)
                
                # GROUND LIGHT SWINGS
                if event.key == self.light_swing_key:
                    self.handle_ground_light(current_time)
                
                # HEAVY SWING
                if event.key == self.heavy_swing_key:
                    self.handle_heavy(current_time)
                
                # BLOCKING START
                if event.key == self.block_key:
                    self.handle_block_start(current_time)
                    
              
            if event.type == pygame.KEYUP:
                # BLOCK STOP
                if event.key == self.block_key:
                    self.handle_block_stop()
                    
            if event.type == pygame.QUIT:
                game.running = False
            
    

            
    def handle_walk(self,screen_width):
        if not self.is_hit and not self.attacking and not self.blocking and not self.stunned:
            self.walk(screen_width)
    
    def handle_run(self,screen_width):
        if not self.is_hit and not self.attacking and not self.blocking and not self.stunned:
            self.run(screen_width)
    
    def handle_gravity(self,screen_height):
        # only applies gravity if not performing an action
        if not self.is_hit and not self.attacking and not self.blocking and not self.stunned:
            self.apply_gravity(screen_height)
        
            
            
    def handle_jump(self):
        if not self.attacking and not self.stunned:
            self.reset_frame()
            self.jump()
                    
    def handle_air_light(self,current_time):
        if current_time - self.last_light >= self.light_cd:
            if not self.attacking and not self.blocking and not self.stunned and self.in_air:
                self.last_light = current_time
                self.reset_frame()
                self.set_attack("d_light")
                        
    def handle_ground_light(self,current_time):
        # NEUTRAL AND SIDE LIGHT
        if current_time - self.last_light >= self.light_cd:
            if not self.attacking and not self.blocking and not self.stunned:
                # checks if player in neutral mode
                if not (self.walking or self.running):
                    self.last_light = current_time
                    self.reset_frame()
                    self.set_attack("n_light")
                            
                elif self.running:
                    self.reset_frame()
                    self.set_attack("s_light")
                    
    def handle_heavy(self,current_time):
        if current_time - self.last_heavy >= self.heavy_cd:
            if not self.attacking and not self.blocking and not self.stunned:
                # checks if player in neutral mode
                if not (self.walking or self.running):
                    self.last_heavy = current_time
                    self.reset_frame()
                    self.set_attack("n_heavy")
                        
                        
    def handle_block_start(self,current_time):
        if current_time - self.last_block >= self.block_cd:
            if not self.attacking and not self.stunned:
                self.last_block = current_time
                self.reset_frame()
                self.blocking = True
                
    def handle_block_stop(self):
        self.blocking = False
        # resets block meter
        self.bp = 0
                        
     
    # displays the current animation sprite to player's hitbox by accessing the current offsets 
    def display_character(self,screen):
        
        # Flips the sprite if self.flip is True
        self.cur_sprite = pygame.transform.flip(self.cur_sprite, self.flip, False)

        if not self.flip:
            # Draws the sprite without flipping
            screen.blit(self.cur_sprite, (self.hitbox.x + self.current_offset[0], self.hitbox.y + self.current_offset[1]))
        else:
            # Draws the flipped sprite with a specific offset
            screen.blit(self.cur_sprite, (self.hitbox.x - self.current_offset[0] - self.cur_sprite.get_width() + 90, self.hitbox.y + self.current_offset[1]))
            
            
            
    
          
        

        
        

        
         
            
            
      
        
        
    
     
            
            
            