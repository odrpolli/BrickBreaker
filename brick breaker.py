#Owen Pollitt, Sean Bell, Gavin Villanueva, Zachary Wong

import pygame, sys, random, time
from pygame.sprite import Sprite

class Brickbreaker:
    """Class manages game behaviour"""

    def __init__(self):
        """initializes game"""
        pygame.init()
        self.settings=Settings()
        # dimensions of game are 1200 pixels by 600 pixels
        self.screen=pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        #Caption of game is 'Brick Breaker!'
        pygame.display.set_caption('Brick Breaker!')
        #paddle
        self.paddle=Paddle(self)
        #ball
        self.balls=pygame.sprite.Group()
        self._create_ball()
        #bricks
        self.bricks=pygame.sprite.Group()
        self._create_grid()
    
    def run_game(self):
        """Main loop"""
        while True:
            self._check_events()
            self.paddle.update()

            self.collisions()

            self._update_balls()
            self._update_screen()
    

    def _check_events(self):
        """response to mouse and keyboard"""
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
            #if player clicks the close button pygame window closes and game ends
                pygame.quit()
                sys.exit()

            elif event.type==pygame.KEYDOWN:
                #Move Right
                if event.key==pygame.K_RIGHT:
                    self.paddle.moving_right=True
                #Move Left
                elif event.key==pygame.K_LEFT:
                    self.paddle.moving_left=True
                
            elif event.type==pygame.KEYUP:
                #Stop Move Right
                if event.key==pygame.K_RIGHT:
                    self.paddle.moving_right=False
                #Stop Move Left
                elif event.key==pygame.K_LEFT:
                    self.paddle.moving_left=False
    
    def collisions(self):
        """tracks the balls collisions"""
        for ball in self.balls.copy():
            for brick in self.bricks.copy():
                if pygame.sprite.spritecollideany(brick, self.balls)!=None:
                    if (abs(brick.rect.top-ball.rect.bottom)<self.settings.collision_precision \
                        or abs(brick.rect.bottom-ball.rect.top)<self.settings.collision_precision):
                        self.bricks.remove(brick)
                        self.settings.score+=self.settings.point_increment
                        self.settings.moving_y=not self.settings.moving_y
                        """randompower=random.randint(0,3)
                        if randompower==1:
                            test=self.paddle.rect.x
                            self.settings.paddle_width+=50
                            self.paddle=Paddle(self)
                            self.paddle.rect.x=test"""
                        
                    elif (abs(brick.rect.right-ball.rect.left)<self.settings.collision_precision \
                          or abs(brick.rect.left-ball.rect.right)<self.settings.collision_precision):
                        self.bricks.remove(brick)
                        self.settings.score+=self.settings.point_increment
                        self.settings.moving_x=not self.settings.moving_x
                        """ randompower=random.randint(0,100)
                        if randompower==1:
                            test=self.paddle.rect.x
                            self.settings.paddle_width+=50
                            self.paddle=Paddle(self)
                            self.paddle.rect.x=test"""

            if ball.rect.right==self.settings.screen_width or ball.rect.left==0:
                self.settings.moving_x=not self.settings.moving_x
            if ball.rect.bottom==self.settings.screen_height:
                self.loss()
            if ball.rect.top==0:
                self.settings.moving_y=not self.settings.moving_y
            
            if pygame.sprite.spritecollideany(self.paddle, self.balls)!=None:
                if abs(self.paddle.rect.top-ball.rect.bottom)<self.settings.collision_precision:
                    self.settings.moving_y=not self.settings.moving_y
                
                
                elif abs(self.paddle.rect.right-ball.rect.left)<self.settings.collision_precision \
                    or abs(self.paddle.rect.left-ball.rect.right)<self.settings.collision_precision:
                        self.settings.moving_x=not self.settings.moving_x
                        self.settings.moving_y=not self.settings.moving_y
                            
        
        
        
    
        
        
    def _update_balls(self):
        """update position of balls"""
        self.balls.update()
        

        # if bricks group is empty creates new grid of bricks
        if not self.bricks:
            self.settings.level+=1
            self._create_grid()
            self.settings.ball_speed+=self.settings.increment_ball_speed
            
                
                
    def _update_screen(self):
        """updates screen"""
        #background colour
        self.screen.fill(self.settings.background_colour)
        #bricks
        self.bricks.draw(self.screen)
        #paddle
        self.paddle.blitme()
        #balls
        self.balls.draw(self.screen)
        
        
        #text
        self.update_text()
        
        
        #prints new screen
        pygame.display.flip()
    
    def _create_ball(self):
        """creates ball"""
        ball=Ball(self)
        self.balls.add(ball)
        
    
    def _create_grid(self):
        """creates grid of bricks"""

        #calculates how many bricks fit on screen
        brick=Brick(self)
        brick_width, brick_height=brick.rect.size
        available_space_x=self.settings.screen_width - int(self.settings.screen_width/6)
        number_bricks_x=available_space_x//(brick_width)

        available_space_y=self.settings.screen_height-int(self.settings.screen_height/2)
        number_bricks_y=available_space_y//(2*brick_height)

        #calls on _create_brick in order for an brick to be placed in assigned position
        for row_number in range(number_bricks_y):
            for brick_number in range(number_bricks_x):
                self._create_brick(brick_number, row_number)
    
    def _create_brick(self, brick_number, row_number):
        """creates brick"""
        brick=Brick(self)
        brick_width, brick_height=brick.rect.size
        brick.x=brick_width+1.1*brick_width*brick_number
        brick.rect.x=brick.x
        brick.y=brick_height+2*brick.rect.height*row_number
        brick.rect.y=brick.y
        self.bricks.add(brick)
    
    def update_text(self):
        self.leveltext = self.settings.font.render(f'Level {self.settings.level}', True, self.settings.text_colour)
        self.levelRect = self.leveltext.get_rect()
        self.levelRect.topleft=(0,0)
        
        self.points=self.settings.font.render(f' Points: {self.settings.score}',True,self.settings.text_colour)
        self.pointsRect=self.points.get_rect()
        self.pointsRect.topright=(self.settings.screen_width,0)
        
        self.screen.blit(self.leveltext, self.levelRect)
        
        self.screen.blit(self.points, self.pointsRect)
    
    def loss(self):
        """message if player loses"""
        self.settings.end_time=time.time()
        self.settings.score+=int(self.settings.end_time-self.settings.start_time)
        message=pygame.image.load('gameover.bmp')
        message=pygame.transform.scale(message, (self.settings.screen_width,self.settings.screen_height))
        self.screen.blit(message, (0,0))
        font=pygame.font.Font(self.settings.style,self.settings.size)
        points=font.render(f' Points: {self.settings.score}',True,self.settings.text_colour)
        pointsRect=points.get_rect()
        pointsRect.center=(self.settings.screen_width/2,self.settings.screen_height/2)
        self.screen.blit(points, pointsRect)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()
        
        
class Settings:
    """A class to store settings for the game"""
    def __init__(self):
        """initializes the games settings"""
        #screen settings
        self.screen_width=1200
        self.screen_height=600
        self.background_colour=(211,211,211)
        self.score=0
        self.start_time=time.time()
        self.end_time=0
        self.level=1
        
        #text settings
        self.style='freesansbold.ttf'
        self.size=32
        self.text_colour=(0,0,0)
        self.font=pygame.font.Font(self.style,self.size)
        
        
        #Ball settings
        self.ball_speed=0.2
        self.ball_width=25
        self.ball_height=25
        self.ball_colour=(255,173,0)
        self.ball_start_rand=300
        self.increment_ball_speed=0.1
        
        #ball motion
        random_motion=[True,False]
        randomnum=random.randint(0,1)
        self.ballmove=True
        self.moving_x=random_motion[randomnum]
        self.moving_y=False
        
        #paddle settings
        self.paddle_width=100
        self.paddle_height=20
        self.paddle_speed=0.8
        
        #Brick settings
        self.brick_width=150
        self.brick_height=30
        self.collision_precision=3
        
        self.point_increment=10
        

class Paddle:
    """This class manages my paddle """
    def __init__(self, game):
        """initializes paddle and starting position"""
        self.settings=game.settings
        self.screen=game.screen
        self.screen_rect=game.screen.get_rect()

        #Loading image
        self.image=pygame.image.load('paddle.bmp')
        #size of image
        self.image=pygame.transform.scale(self.image, (game.settings.paddle_width,game.settings.paddle_height))
        self.rect=self.image.get_rect()

        #location of image
        self.rect.midbottom=self.screen_rect.midbottom

        #movement flag
        self.moving_right=False
        self.moving_left=False
        self.posx=self.rect.x

        
    def update(self):
        """update paddle position based on movement flag"""
        #stops paddle from leaving screen, change values to increase or decrease speed
        if self.moving_right and self.rect.right<self.screen_rect.right:
            self.posx+=self.settings.paddle_speed
            self.rect.x=self.posx
        if self.moving_left and self.rect.left>self.screen_rect.left:
            self.posx-=self.settings.paddle_speed
            self.rect.x=self.posx

    def blitme(self):
        """Draws paddle"""
        self.screen.blit(self.image, self.rect)


class Brick(Sprite):
    """represents bricks"""
    def __init__(self,game):
        """initializes bricks' settings"""
        super().__init__()
        self.screen=game.screen
        self.settings=game.settings

        #star image, size, location
        self.image=pygame.image.load('brick.bmp')
        self.image=pygame.transform.scale(self.image, (game.settings.brick_width,game.settings.brick_height))
        self.rect=self.image.get_rect()

        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
        self.x=float(self.rect.x)
        self.y=float(self.rect.y)

class Ball(Sprite):
    """represents ball"""
    def __init__(self,game):
        """initializes ball settings"""
        super().__init__()
        #initializes ball and starting position
        self.screen=game.screen
        self.screen_rect=game.screen.get_rect()
        self.settings=game.settings

        #Loading image
        self.image=pygame.image.load('ball.bmp')
        #size of image
        self.image=pygame.transform.scale(self.image, (game.settings.ball_width,game.settings.ball_height))
        self.rect=self.image.get_rect()

        #location of image (midbottom + paddle hieght so it starts above paddle)
        random_location=random.randint(-game.settings.ball_start_rand,game.settings.ball_start_rand)
        self.rect.midbottom=(self.screen_rect.midbottom[0]+random_location,self.screen_rect.midbottom[1]-game.settings.ball_height)
        
        #variables to store float location of ball (allows the ball to travel slower with decimal speeds)
        self.posx=self.rect.x
        self.posy=self.rect.y


    def update(self):
        """move ball to the left"""
        if self.settings.ballmove==True:
            if self.settings.moving_x and self.rect.right<self.screen_rect.right:
                self.posx+=self.settings.ball_speed
                self.rect.x=self.posx
            if not self.settings.moving_x and self.rect.left>self.screen_rect.left:
                self.posx-=self.settings.ball_speed
                self.rect.x=self.posx
            if self.settings.moving_y and self.rect.bottom<self.screen_rect.bottom:
                self.posy+=self.settings.ball_speed
                self.rect.y=self.posy
            if not self.settings.moving_y and self.rect.top>self.screen_rect.top:
                self.posy-=self.settings.ball_speed
                self.rect.y=self.posy
            
        
        

if __name__=='__main__':  
    #Calling an instance of the game
    game_instance=Brickbreaker()
    game_instance.run_game()
    
