import pygame
import random
import os
#Game Loop 
#def gameloop():
WIDTH = 480
HEIGHT = 800
FPS = 50

#set up assets folder
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "image")



#initialize pygame
pygame.init() 
pygame.mixer.init()
#create window 
screen  = pygame.display.set_mode((WIDTH, HEIGHT)) #set the demensions of the screen
pygame.display.set_caption("GALACTICMOONHUNT")  #set/display the title of the game
icon = pygame.image.load(os.path.join(img_folder, "moon.png")).convert()#load the game icon

pygame.display.set_icon(icon) #display the icon
clock = pygame.time.Clock()
score = 0 #set score = 0 when pygame starts up

font_name = pygame.font.match_font("arial") #get the arial font from your computer (or the closest match)
def draw_text(surface, text, size, x, y): #draw text on the screen 
    font= pygame.font.Font(font_name, size) #create font with the parameters font name and size
    text_surface = font.render(text, True, (0,255,0)) #make a surcafe for the text on the screen, true = anti-alias
    text_rect = text_surface.get_rect() #make a rectangle for the text to be able to place the text
    text_rect.midtop = (x,y) #set the location of the text to the midle of the rectangle
    surface.blit(text_surface, text_rect) #draw onto the screen

def show_gameover_screen():
    background(backgroundx, backgroundy)
    draw_text(screen, "Score: "+str(score), 50, WIDTH/2, 10) #displays the score
    draw_text(screen, "GALACTICMOON", 64, WIDTH/2, HEIGHT/4) #show game over
    draw_text(screen, "Press W to move up", 40, WIDTH/2, HEIGHT/2 -70) # DISPLAY INSTRUCTION
    draw_text(screen, "Press S to move down", 40, WIDTH/2, HEIGHT/2 -30) # DISPLAY INSTRUCTION
    draw_text(screen, "Press A to move left", 40, WIDTH/2, HEIGHT/2 +10) # DISPLAY INSTRUCTION
    draw_text(screen, "Press D to move right", 40, WIDTH/2, HEIGHT/2 + 50) # DISPLAY INSTRUCTION
    draw_text(screen, "Press UP-ARROW to shoot", 40, WIDTH/2, HEIGHT/2 + 90) # DISPLAY INSTRUCTION
    draw_text(screen, "PRESS SPACE BEGIN", 40, WIDTH/2, HEIGHT - 100) #DISPLAY INSTRUCTIONS
    pygame.display.flip() #allow users to see the endgame screen
    waiting = True #set a new loop
    while waiting:
        clock.tick(FPS) #speed at which the loop if gone through
        for event in pygame.event.get(): #quit if the player exits the game
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP: #start the game if the player presses a button
                if event.key == pygame.K_SPACE:
                    waiting = False


class Player(pygame.sprite.Sprite): #set up player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "spaceship_2.png")).convert() ## 50 by 50
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.radius = 22
        #pygame.draw.circle(self.image, (0,0,0), self.rect.center, self.radius)
        self.rect.centerx = WIDTH/2 #X position
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0 #set side to side speed
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -20
        if keystate[pygame.K_d]:
            self.speedx = 20
        self.rect.x += self.speedx #moves player by x speed
        if keystate[pygame.K_w]:
            self.speedy = -20
        if keystate[pygame.K_s]:
            self.speedy = 20
        self.rect.y += self.speedy #moves player by y speed
        if self.rect.right > WIDTH:
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.right = WIDTH
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = HEIGHT
    
    def shootup(self): #define the shooting funtion
        bullet = Bullet(self.rect.centerx, self.rect.top) #create a bullet and the bullets location
        all_sprites.add(bullet) #add the bullet to the app_sprites group
        bullets.add(bullet) #add the bullet to the bullets group


class Mob(pygame.sprite.Sprite): #set up enemy
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "moon.png")).convert() ## 54 by 54
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.radius = 24
        #pygame.draw.circle(self.image, (0,0,255), self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width) #enemy spawn random on x axis
        self.rect.y = random.randrange(-400, -50)
        self.speedy = random.randrange(6,20)
        self.speedx = random.randrange(-10, 10)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width) #enemy spawn random on x axis
            self.rect.y = random.randrange(-400, -50)
            self.speedy = self.speedy + random.randrange(-1,2)
            self.speedx = random.randrange(-12, 12)
        if self.rect.left <0:
            self.speedx = random.randrange(4, 14)
        if self.rect.right > WIDTH:
            self.speedx = random.randrange(-14, -4)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20)) #set bullet image
        self.image.fill((255,0,0))  #sets the color of the bullet image
        self.rect = self.image.get_rect() #gives the image a rectangle
        self.radius = 10
        #pygame.draw.circle(self.image, (0,0,255), self.rect.center, self.radius)
        self.rect.bottom = y #sets the y cordinate of the bullet
        self.rect.centerx = x #sets the x cordinate of the bullet 
        self.speedy = -30 #set the bullets y speed
        self.speedx = 0 
    

    def update(self): 
        self.rect.y += self.speedy #move the bullet along the y axis
        #kill the bullet if it moves off the screen
        if self.rect.bottom < 0: #if the bottom on the moves pat the top of the screen
            self.kill()


#background
backgroundImg = pygame.image.load(os.path.join(img_folder, "space.jpg")).convert() #set the background image
backgroundx = random.randint(-4910, -20) #set a random location for the nackground on the x axis
backgroundy = random.randint(-2700, 0)#set a random location for the nackground on the y axis
backgroundy_change = 0 #the background on the y axis yet doesnt move yet
backgroundx_change = 0 #the background on the x axis yet doesnt move yet

def background(x, y):
    screen.blit(backgroundImg, (x, y)) #draw the background onto the screen

    

#Game Loop
game_over = True #determines whether to show the game over screen or not
running = True
while running: 
    if game_over:
        show_gameover_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)  
        bullets = pygame.sprite.Group()
        for i in range(7): #create 7 enemies
            mob = Mob() #create an enemy
            all_sprites.add(mob) #add an enemy to the all sprites group
            mobs.add(mob) #add an enemy to the mobs group
        #set score = 0 when game starts
        score = 0

    #keep loop running at the right speed
    clock.tick(FPS)
    #process input(events)
    for event in pygame.event.get():
        #check for closing the window
        if event.type == pygame.QUIT: #if the user presses the exit out button
            running = False    #the game stops running

    #press button to shoot
        if event.type == pygame.KEYDOWN: #if the user presses down a key
            #shoot bullet
            if event.key == pygame.K_UP: #if user presses the up arrow
                player.shootup()
        if event.type == pygame.KEYUP: #if the usser lifts up a key
            if event.key == pygame.K_a or pygame.K_d: #if the user releases the a or d key
                backgroundx_change = 0 #the background stops moving left or right
            if event.key == pygame.K_s or pygame.K_w: #if the user releases the s or w key
                backgroundy_change = 0 #the background stops moving or or down
    #set background movement
            
    keystates = pygame.key.get_pressed()
    if keystates[pygame.K_a]:
        backgroundx_change = 30  
    if keystates[pygame.K_d]:
        backgroundx_change = -30
    if keystates[pygame.K_w]:
        backgroundy_change = 30
    if keystates[pygame.K_s]:
        backgroundy_change = -30
    backgroundx += backgroundx_change
    backgroundy += backgroundy_change
    #BACKGROUND MOVEMENT
    if backgroundx < -4910: #set the left  xboundary for the background
        backgroundx = -3340
    if backgroundx > -20: #set the right x boundary for the background
        backgroundx = -770
    if backgroundy > 0: 
        backgroundy = -2700 #set the upper y boundary for the background
    if backgroundy < -2700:
        backgroundy = 0 #set the lower y boundary for the background


    #Update
    all_sprites.update()
    

    #check to see if a bullet hit the mob player
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True) #delete bullet and mob if they collide
    for hit in hits: #make new mobs when old ones are shot
        m = Mob()
        all_sprites.add(m) #add the mob to tha sll srpites list
        mobs.add(m) #add mob to the mob list
        score += 100
    #check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle) #check the sprite againt the group
    
    if hits: #turn off game of you collide
        game_over = True
    
    #Draw/render
    #screen.fill((0,0,0)) #set the screen .... not needed?
    background(backgroundx, backgroundy) #call the funtion that draws the background 
    all_sprites.draw(screen) #draw all the spites onto the screen
    draw_text(screen, "Score: "+str(score), 50, WIDTH/2, 10) #call the drawtext funtion, screen if the surface, string of the score is the text
    #do after drawing everything
    pygame.display.flip() #update the screen to show the drawings
    
pygame.quit()




