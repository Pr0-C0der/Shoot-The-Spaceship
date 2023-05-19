import pygame
import sys
import os
pygame.font.init() #Intialising the font
pygame.mixer.init() #Initialising the music


# Setting the windows size
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


# Setting the name of the game
pygame.display.set_caption("Shoot the SpaceShip!")
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
# Since the while loop is updating constantly, it depends on the speed of machine as how many times the
# while loop is getting executed. Hence, it will be different on different machines. To make it consistent,
# on every machine, we introduce FPS(frames per second). It restricts the updation to certain limit (in this
# case it is 60 frames per second)
FPS = 80


SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
# We use os.path.join as on different operating systems the separators might be different
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_yellow.png")
)
YELLOW_SPACESHIP = pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
)  # Resizing the image
YELLOW_SPACESHIP = pygame.transform.rotate(YELLOW_SPACESHIP,90) #Rotating image by 90 degrees
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
)  # Resizing the image
RED_SPACESHIP = pygame.transform.rotate(RED_SPACESHIP,270)


VEL = 5 #Velocity at which we want to move our spaceship


MAX_BULLETS = 5 #Maximum number of bullets a spaceship can fire
BULLET_VEL = 7 #Velocity of the bullets


BORDER = pygame.Rect(WIDTH//2 - 5,0,10,HEIGHT) #This border will not let the spaceships pass each other


#Defining events where the spaceships are hit
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


#Loading the Space Background
SPACE = pygame.image.load(os.path.join('Assets','space.jpg'))
SPACE = pygame.transform.scale(SPACE,(WIDTH,HEIGHT))


#Defining the Font which we have to display
HEALTH_FONT = pygame.font.SysFont('comicsans',40)
WINNER_FONT = pygame.font.SysFont('comicsans',100)

#Loading the sound we want to play
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets','shoot_bullet.mp3'))


def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
    WIN.blit(SPACE,(0,0)) #Loading the space background
    pygame.draw.rect(WIN,BLACK,BORDER) #Loading the border to separate the spaceships

    #Rendering text to display the health
    red_health_text = HEALTH_FONT.render("Health : " + str(red_health),1,WHITE)
    yellow_health_text = HEALTH_FONT.render("Health : " + str(yellow_health),1,WHITE)
    
    #Displaying the health
    WIN.blit(red_health_text,(WIDTH-red_health_text.get_width()-10,10))
    WIN.blit(yellow_health_text,(10,10))

    #Drawing the spaceships on the screen
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))  
    WIN.blit(RED_SPACESHIP, (red.x, red.y)) 

    #Drawing the bullets
    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet) 

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)
    pygame.display.update()  # Note that whenever your display changes you have to run this command

def actions(red,yellow):
    #Getting which keys were pressed
    keys_pressed = pygame.key.get_pressed()

    #FOR YELLOW
    if(keys_pressed[pygame.K_a] and yellow.x-VEL>0):
        yellow.x-=VEL
    
    #Recatangle has its width and the 0,0 (origin) of a rectangle starts form left top corner. Hence we also
    #have to check for the width 
    if(keys_pressed[pygame.K_d] and yellow.x+VEL+yellow.width<BORDER.x):
        yellow.x+=VEL
    if(keys_pressed[pygame.K_w] and yellow.y-VEL>0):
        yellow.y-=VEL

    #The yellow ship was passing the border hence to prevent that we just add some (15) pixels to prevent
    #that.
    if(keys_pressed[pygame.K_s] and yellow.y+VEL+yellow.height<HEIGHT-15):
        yellow.y+=VEL

    #FOR RED
    #The red spaceship was stopping much nearer to the border than the yellow spaceship, hence to 
    #prevent that we add extra 20 pixels
    if(keys_pressed[pygame.K_LEFT]and red.x-VEL>BORDER.x+BORDER.width):
        red.x-=VEL
    if(keys_pressed[pygame.K_RIGHT] and red.x+VEL+red.width<WIDTH):
        red.x+=VEL
    if(keys_pressed[pygame.K_UP] and red.y-VEL>0):
        red.y-=VEL
    if(keys_pressed[pygame.K_DOWN]and red.y+VEL+red.height<HEIGHT-15):
        red.y+=VEL
    return red,yellow


def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    #Checking for all the bullets
    for bullet in yellow_bullets:
        bullet.x+=BULLET_VEL #Updating the bullet velocity
        
        if(red.colliderect(bullet)): #Checking if the red spaceship has collided with the bullet
            #If bullet has collided with the spaceship then we fire event RED_HIT indicating that
            #red spaceship was hit and remove the bullet from the list
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif (bullet.x>WIDTH):
            #If the bullet passes through the screen, we remove the bullet from the lisr
            yellow_bullets.remove(bullet)


    for bullet in red_bullets:
        bullet.x-=BULLET_VEL
        
        if(yellow.colliderect(bullet)):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif (bullet.x < 0):
            red_bullets.remove(bullet)


def draw_winner(text):
    #Rendering the message we want to display
    winner_text = WINNER_FONT.render(text,1,WHITE)

    #Displaying it on the screen
    WIN.blit(winner_text,(WIDTH//2 - winner_text.get_width()//2,HEIGHT//2 - winner_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000) #As soon as someone wins we display the text and wait for 5s the exit the game


def main():
    red_health = 10
    yellow_health = 10
    yellow_bullets = []
    red_bullets = []
    #We need the spaceship to be moving. Hence we need rectangles to represent the spaceships
    red = pygame.Rect(700,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    run = True
    clock = pygame.time.Clock() 
    while run:
        clock.tick(FPS) #For FPS
        # Loop through all the events in pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # First check if the user wants to exit
                run = False
            
            #pygame.KEYDOWN means that some key is pressed down
            if event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_LCTRL and len(yellow_bullets)<MAX_BULLETS):
                    BULLET_FIRE_SOUND.play()
                    #Creating a bullet. Setting its position so that it only fires from middle of the 
                    #spaceship and defining the size of bullet
                    bullet = pygame.Rect(yellow.x+yellow.width,yellow.y+yellow.height//2-2,10,5)
                    yellow_bullets.append(bullet)
                
                if(event.key == pygame.K_RCTRL and len(red_bullets)<MAX_BULLETS):
                    BULLET_FIRE_SOUND.play()
                    #Creating a bullet. Setting its position so that it only fires from middle of the 
                    #spaceship and defining the size of bullet
                    bullet = pygame.Rect(red.x,red.y+red.height//2 - 2,10,5)
                    red_bullets.append(bullet)
            
            if (event.type == RED_HIT):
                red_health-=1
                BULLET_HIT_SOUND.play() #Playing the sound when bullet hits red spaceship
            if (event.type == YELLOW_HIT):
                yellow_health-=1
                BULLET_HIT_SOUND.play()
        
        #Checking if we have a winner
        winner_text = ""
        if(red_health<=0):
            winner_text = "Red is Winner"
        if(yellow_health<=0):
            winner_text = "Yellow is Winner"

        if(winner_text!=''):
            draw_winner(winner_text) #If we have a winner then we just draw the winning text and end
            break

        #Tracking the actions of red and yellow spaceships
        red,yellow = actions(red,yellow)

        #Handling the bullets 
        handle_bullets(yellow_bullets,red_bullets,yellow,red)

        #Updating the screen
        draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health)

    pygame.quit()  # Quitting the game in the end
    sys.exit()


if __name__ == "__main__":
    main()
