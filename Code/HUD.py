import pygame


class HUD:
    def __init__(self,p1,p2):
        pygame.init()
        self.player1 = p1
        self.player2 = p2
        self.timer = 60
        self.sudden_death = False
        
        self.last_timer_update = 0
        self.font = pygame.font.Font(None, 70)
        
    def draw_healthbars(self,screen):
        
        player1HP = self.player1.get_hp()
        player2HP = self.player2.get_hp()
     
        red = (255,0,0)
        green = (0,255,0)
        
 
        # draw underlying red polygon for player1
        pygame.draw.polygon(screen,red,((60,20),(20,60),(420,60),(460,20)))
        
        pygame.draw.polygon(screen,red,((1210,20),(1250,60),(850,60),(810,20)))
        
        #draw underlying red polygon for player2
        
        # draw overlaying green polygon for health, dependent on the current health ratio to the width
        if player1HP > 0:
            p1_health_width = (player1HP/100) * 400 # 400 = width
            pygame.draw.polygon(screen,green,((460-p1_health_width,20),(420-p1_health_width,60),(420,60),(460,20)))
            
        if player2HP > 0:
            p2_health_width = (player2HP/100) * 400 # 400 = width
            pygame.draw.polygon(screen,green,((850,60),(810,20),(810+p2_health_width,20),(850+p2_health_width,60)))
            
            
            
    def draw_blockbars(self,screen):
        
        black = (0,0,0)
        orange = (255,172,0)
        
        player1BP = self.player1.get_bp()
        player2BP = self.player2.get_bp()
        
        # underlying polygon for player 1
        pygame.draw.polygon(screen,black,((40,80),(20,100),(220,100),(240,80)))
        
        # player 2 underlying polygon
        pygame.draw.polygon(screen,black,((1230,80,),(1250,100),(1050,100),(1030,80)))
        
        
        
        if player1BP > 0 and player1BP <= 50:
            p1_block_width = (player1BP/20)*200
            pygame.draw.polygon(screen,orange,((40,80),(20,100),(20+p1_block_width,100),(40+p1_block_width,80)))
            
        if player2BP > 0 and player2BP <= 50:
            p2_block_width = (player2BP/20)*200
            pygame.draw.polygon(screen,orange,((1230,80),(1250,100),(1250 - p2_block_width,100),(1230-p2_block_width,80)))
            
        
            
    def update_timer(self):
        # reduces timer by 1 every time a second passes
        current_time = pygame.time.get_ticks()
        if self.timer > 0 :
            if current_time - self.last_timer_update >= 1000:
                self.timer -= 1
                self.last_timer_update = current_time
                if self.timer == 0:
                    self.sudden_death = True
                    self.player1.sudden_death_damage()
                    self.player2.sudden_death_damage()
        
            
    
    def draw_timer(self,screen):
        red = (255,0,0)
        white = (255,255,255)
        # renders the font object using the timer
        if not self.sudden_death:
            text = self.font.render(str(self.timer), True, white)
        else:
            text = self.font.render(str(self.timer),True,red)
        # places the timer between the health bars in the middle
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 310))
        screen.blit(text, text_rect)
        pygame.display.flip()
        
        # updates timer
        self.update_timer()
        
        
        
        
        
    def reset(self):
        self.timer = 60
        self.sudden_death = False

        
        
    def render(self,screen):
        self.draw_healthbars(screen)
        self.draw_blockbars(screen)
        self.draw_timer(screen)