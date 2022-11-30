#Owen Pollitt, Sean Bell, Zackary Wong, Gavin Villanueva
#CHE 120-Project      Brickbreaker from Scratch

#importing modeules, pygame, sys, random, time and Sprite(from pygame)
import pygame, sys, random, time
from pygame.sprite import Sprite

class Brickbreaker:
    """Main Class that manages Brickbreaker game"""

    def __init__(self):
        """initializes game"""
        #initializes pygame
        pygame.init()
        #calls the class Settings, in order to access game settings
        self.settings=Settings()
        #sets screen size and caption
        self.screen=pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption('Brick Breaker!')
        #paddle
        self.paddle=Paddle(self)
        #creates a sprite object for balls and creates balls, sprite object allows possibility of increasing number of balls
        self.balls=pygame.sprite.Group()
        self._create_ball()
        #creates sprite object for bricks and creates the grid of bricks
        self.bricks=pygame.sprite.Group()
        self._create_grid()
    
    def run_game(self):
        """Main game loop"""
        #calls various methods in a loop to update and run the game
        while True:
            self._check_events()
            self.paddle.update()
            self.collisions()
            self._update_balls()
            self._update_screen()
    

    def _check_events(self):
        """response to mouse and keyboard inputs"""
        #loop monitoring player inputs
        for event in pygame.event.get():
            #if player clicks the exit button pygame window closes and game ends
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            #pressing keys
            elif event.type==pygame.KEYDOWN:
                #Move Right
                if event.key==pygame.K_RIGHT:
                    self.paddle.moving_right=True
                #Move Left
                elif event.key==pygame.K_LEFT:
                    self.paddle.moving_left=True
            
            #releasing keys
            elif event.type==pygame.KEYUP:
                #Stop Move Right
                if event.key==pygame.K_RIGHT:
                    self.paddle.moving_right=False
                #Stop Move Left
                elif event.key==pygame.K_LEFT:
                    self.paddle.moving_left=False
    
    def collisions(self):
        """Tracks ball collisions with side of screen, bricks and paddle"""
        for ball in self.balls.copy():
            #loops through bricks to determine ball and brick collisions
            for brick in self.bricks.copy():
                if pygame.sprite.spritecollideany(brick, self.balls)!=None:
                    
                    #collisions with top and bottom of bricks
                    if (abs(brick.rect.top-ball.rect.bottom)<self.settings.collision_precision \
                        or abs(brick.rect.bottom-ball.rect.top)<self.settings.collision_precision):
                        #removes brick and adds to score
                        self.bricks.remove(brick)
                        self.settings.score+=self.settings.point_increment
                        #changes y direction
                        self.settings.moving_y=not self.settings.moving_y
                        #calls powerup method
                        self.powerup()
                        
                    #collisions with sides of bricks
                    elif (abs(brick.rect.right-ball.rect.left)<self.settings.collision_precision \
                          or abs(brick.rect.left-ball.rect.right)<self.settings.collision_precision):
                        #removes brick and adds to score
                        self.bricks.remove(brick)
                        self.settings.score+=self.settings.point_increment
                        #changes y direction
                        self.settings.moving_x=not self.settings.moving_x
                        #calls powerup method
                        self.powerup()
            #checks for collisions with side of screen and changes x direction
            if ball.rect.right==self.settings.screen_width or ball.rect.left==0:
                self.settings.moving_x=not self.settings.moving_x
            #if ball hits the bottom of screen game ends
            if ball.rect.bottom==self.settings.screen_height:
                self.loss()
            #if ball hits top of screen y direction changes
            if ball.rect.top==0:
                self.settings.moving_y=not self.settings.moving_y
            
            #collisions between ball and paddle
            if pygame.sprite.spritecollideany(self.paddle, self.balls)!=None:
                #top of paddle with bottom of ball
                if abs(self.paddle.rect.top-ball.rect.bottom)<self.settings.collision_precision:
                    self.settings.moving_y=not self.settings.moving_y
                
                #sides of paddle with ball
                elif abs(self.paddle.rect.right-ball.rect.left)<self.settings.collision_precision \
                    or abs(self.paddle.rect.left-ball.rect.right)<self.settings.collision_precision:
                        self.settings.moving_x=not self.settings.moving_x
                        self.settings.moving_y=not self.settings.moving_y
                            
        
        
    def powerup(self):
        """1% chance of a powerup that increases the size of the paddle"""
        if random.randint(0,self.settings.powerchance)==1:
            #gets coordinates of paddle
            coord=((self.paddle.rect.right+self.paddle.rect.left)/2,600)
            #increases paddle width
            self.settings.paddle_width+=50
            #maintains the paddles coords when a new paddle with a new size is created
            self.settings.paddlerect=coord
            self.paddle=Paddle(self)
            
    def reset_paddle(self):
        """resets paddle width at every level"""
        #gets coordinates of paddle
        coord=((self.paddle.rect.right+self.paddle.rect.left)/2,600)
        #resets paddle width
        self.settings.paddle_width=self.settings.reset_width
        #maintains paddle coordinates when a new paddle is creates
        self.settings.paddlerect=coord
        self.paddle=Paddle(self)
    
        
        
    def _update_balls(self):
        """update position of balls"""
        #calls update method from class balls
        self.balls.update()
        

        # if bricks group is empty creates new grid of bricks, increases ball speed, increases level and resets paddle width
        if not self.bricks:
            self.settings.level+=1
            self._create_grid()
            self.settings.ball_speed+=self.settings.increment_ball_speed
            self.reset_paddle()
            
                
                
    def _update_screen(self):
        """updates screen"""
        #fills background colour
        self.screen.fill(self.settings.background_colour)
        #draws bricks
        self.bricks.draw(self.screen)
        #draws paddle
        self.paddle.blitme()
        #draaws ball
        self.balls.draw(self.screen)
        #update text
        self.update_text()
        #prints new screen
        pygame.display.flip()