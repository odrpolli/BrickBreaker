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
        
    def _create_ball(self):
        """this function creates the object ball"""
        #the variable ball is an element of the class Ball
        ball=Ball(self)
        self.balls.add(ball)
        
    
    def _create_grid(self):
        """this function creates grid of the bricks"""
        
        #used try and error method to find the rows and columns of bricks that work best
        available_space_x=self.settings.screen_width - int(self.settings.screen_width/6)
        number_bricks_x=available_space_x//(self.settings.brick_width)

        available_space_y=self.settings.screen_height-int(self.settings.screen_height/2)
        number_bricks_y=available_space_y//(2*self.settings.brick_height)

        #calls on _create_brick in order for a brick to be placed in assigned position
        for row_number in range(number_bricks_y):
            for brick_number in range(number_bricks_x):
                self._create_brick(brick_number, row_number)
    
    def _create_brick(self, brick_number, row_number):
        """this function creates the bricks"""
        #the variable brick is an element of the class Brick
        brick=Brick(self)
        #the width and height of the brick gives the size of the rectangular brick
        brick_width, brick_height=brick.rect.size
        #used try n error to find the x coordinates of the bricks
        brick.rect.x=brick_width+1.1*brick_width*brick_number
        #used try n error to find the y coordinates of the bricks
        brick.rect.y=brick_height+2*brick.rect.height*row_number
        self.bricks.add(brick)
    
    def update_text(self):
        """"this function updates the texts including the level and points"""
        self.leveltext = self.settings.font.render(f'Level {self.settings.level}', True, self.settings.text_colour)
        self.levelRect = self.leveltext.get_rect()
        #enters the coorinate of the level text
        self.levelRect.topleft=(0,0)
        
        self.points=self.settings.font.render(f' Points: {self.settings.score}',True,self.settings.text_colour)
        self.pointsRect=self.points.get_rect()
        #enters the coorinate of the points text
        self.pointsRect.topright=(self.settings.screen_width,0)
        
        #display both texts on the screen
        self.screen.blit(self.leveltext, self.levelRect)
        self.screen.blit(self.points, self.pointsRect)
    
    def loss(self):
        """this function displays a message if the player loses"""
        #changes the end time and score on settings
        self.settings.end_time=time.time()
        self.settings.score+=int(self.settings.end_time-self.settings.start_time)
        #uploads the image gameover as the message
        message=pygame.image.load('gameover.bmp')
        message=pygame.transform.scale(message, (self.settings.screen_width,self.settings.screen_height))
        #enters the coorinate of the message
        self.screen.blit(message, (0,0))
        font=pygame.font.Font(self.settings.style,self.settings.size)
        points=font.render(f' Points: {self.settings.score}',True,self.settings.text_colour)
        pointsRect=points.get_rect()
        pointsRect.center=(self.settings.screen_width/2,self.settings.screen_height/2)
        #displays the player's final points
        self.screen.blit(points, pointsRect)
        pygame.display.flip()
        #3 seconds before user can exit the game
        time.sleep(3)
        pygame.quit()
        sys.exit()        
        
        
        
        
        
#creating the function for the settings of the game       
class Settings:
    """A class to store settings for the game"""
    #defining the function 
    def __init__(self):
        """initializes the games settings"""
        #screen width and height settings
        self.screen_width=1200
        self.screen_height=600
        #screens background colour during the game (grey)
        self.background_colour=(211,211,211)
        #The inital score begining the game
        self.score=0
        #creating a timer for the duration of time spent in the game
        self.start_time=time.time()
        self.end_time=0
        #The inital level begining the game 
        self.level=1
        
        #font style and size
        self.style='freesansbold.ttf'
        self.size=32
        self.text_colour=(0,0,0)
        self.font=pygame.font.Font(self.style,self.size)
        
        
        #Ball settings, speed,size, colour(yellow)
        self.ball_speed=0.6
        self.ball_width=25
        self.ball_height=25
        self.ball_colour=(255,173,0)
        self.ball_start_rand=300
        #increases the ball speed by 0.1 per round complete
        self.increment_ball_speed=0.25
        
        #ball motion
        random_motion=[True,False]
        randomnum=random.randint(0,1)
        #ensuring that the ball does indeed move 
        self.ballmove=True
        #ball changes motion in the x direction
        self.moving_x=random_motion[randomnum]
        #ball does not change motion in the y direction
        self.moving_y=False
        
        #paddle settings
        #resets width of the paddle after each round
        self.reset_width=100
        #creating the inital padddle width, height, speed, and the location
        self.paddle_width=100
        self.paddle_height=20
        self.paddle_speed=1.5
        self.paddlerect=(600,600)
        
        #Brick settings
        #creating the bricks width, height, and precision needed to accept the brick has indeed been hit by the ball
        self.brick_width=150
        self.brick_height=30
        self.collision_precision=3
        #increases points per brick hit
        self.point_increment=10
        #probabilty of getting a powerup (1/20)
        self.powerchance=20
        
        
        
        
        
        
#creating the class and the import of sprite 
class Brick(Sprite):
    """represents bricks"""
    #initializes the attributes of the class brick
    def __init__(self,game):
        """initializes bricks' settings"""
        #inheriting the attributes of the import sprite
        super().__init__()
        self.settings=game.settings

        #star image, size, location
        self.image=pygame.image.load('brick.bmp')
        self.image=pygame.transform.scale(self.image, (game.settings.brick_width,game.settings.brick_height))
        self.rect=self.image.get_rect()
       
        #the location of x and y 
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height


class Paddle:
    """This class manages the paddle for the brickbreaker game"""
    def __init__(self, game):
        """initializes paddle and paddle starting position"""
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
        self.rect.midbottom=self.settings.paddlerect 

        #movement flag
        self.moving_right=False
        self.moving_left=False
        #variable posx is used to allow float speed values
        self.posx=self.rect.x

        
    def update(self):
        """update paddle position based on movement flag"""
        #stops paddle from leaving screen, change values to increase or decrease speed
        #moving right
        if self.moving_right and self.rect.right<self.screen_rect.right:
            self.posx+=self.settings.paddle_speed
            self.rect.x=self.posx
        #moving left
        if self.moving_left and self.rect.left>self.screen_rect.left:
            self.posx-=self.settings.paddle_speed
            self.rect.x=self.posx

    def blitme(self):
        """Draws paddle on screen"""
        self.screen.blit(self.image, self.rect)



    
#Creating the class and the import of Ball sprite.
class Ball(Sprite):
    """Properties of the ball."""
    def __init__(self,game):
        """Initializes the ball settings."""
        
        #Initializes all the inherited properties of "class Ball" from sprite.
        super().__init__()
        
        #Initializes ball and starting position.
        self.screen=game.screen
        self.screen_rect=game.screen.get_rect()
        self.settings=game.settings

        #Loads the image of the ball.
        self.image=pygame.image.load('ball.bmp')
        
        #Refers from the values of the height and width from the settings class
        self.image=pygame.transform.scale(self.image, (game.settings.ball_width,game.settings.ball_height))
        self.rect=self.image.get_rect()

        #location of image (midbottom + paddle height so it starts above paddle)
        random_location=random.randint(-game.settings.ball_start_rand,game.settings.ball_start_rand)
        self.rect.midbottom=(self.screen_rect.midbottom[0]+random_location,self.screen_rect.midbottom[1]-game.settings.ball_height)
        
        #variables to store float location of ball (allows the ball to travel slower with decimal speeds)
        self.posx=self.rect.x
        self.posy=self.rect.y


    def update(self):
        """Determines the movement of the ball."""
        
        #If the ball does indeed move the following will occur.
        #Keeps the ball inbound of the screen.
        if self.settings.ballmove==True:
            
            #If "moving_x" is true from the settings class, then the ball moves
            #to the right. Then ensures the ball stays in the vicinity of the 
            #screen.
            if self.settings.moving_x and self.rect.right<self.screen_rect.right:
                self.posx+=self.settings.ball_speed
                self.rect.x=self.posx
            
            #If "moving_x" is true from the settings class, then the ball moves
            #to the left. Ensures the ball stays within the vicinity of the 
            #screen.
            if not self.settings.moving_x and self.rect.left>self.screen_rect.left:
                self.posx-=self.settings.ball_speed
                self.rect.x=self.posx
                
            #If "moving_y" is true from the settings class, then the ball moves
            #to the downward. Ensures the ball stays within the vicinity of the 
            #screen.
            if self.settings.moving_y and self.rect.bottom<self.screen_rect.bottom:
                self.posy+=self.settings.ball_speed
                self.rect.y=self.posy
                
            #If "moving_y" is true from the settings class, then the ball moves
            #to the upward. Ensures the ball stays within the vicinity of the 
            #screen.
            if not self.settings.moving_y and self.rect.top>self.screen_rect.top:
                self.posy-=self.settings.ball_speed
                self.rect.y=self.posy



if __name__=='__main__':  
    #Calling an instance of the game
    game_instance=Brickbreaker()
    game_instance.run_game()
    
    