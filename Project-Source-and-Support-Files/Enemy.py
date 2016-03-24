import pygame
import math
import random
from GameSprite import GameSprite
from Bullet import Enemy1BulletMid
from Bullet import Enemy1BulletLeft
from Bullet import Enemy1BulletRight
from Bullet import Enemy2Bullet
from Bullet import Enemy3Bullet
from Bullet import BossBullet1
from Bullet import BossBullet2
from Bullet import BossBullet3
from Bullet import BossBullet4

class Enemy(GameSprite):

    def __init__(self,x,y):
        #enemy's bullet sprite group
        self.bullets = pygame.sprite.Group()
        self.bulletTimer = 0

        super(Enemy, self).__init__(x, y, self.image, self.width/2)
        self.updateRect()

    def getEnemyBounds(self):
        #gets bounds of bullet
        (x0, y0) = (self.x-self.width/2, self.y-self.height/2)
        (x1, y1) = (self.x + self.width/2, self.y + self.height/2)
        return (x0, y0, x1, y1)

class Enemy1(Enemy):

    def __init__(self,x,y,direction):
        #enemy 1 moves left or right and down
        self.direction = direction
        self.size = 20
        self.score = 100
        self.color = (255,0,255)
        self.health = 25
        self.bulletSize = 10
        ''' Source: http://www.rpglegion.com/ff6/monsters/airforce.png
        This is a Final Fantasy 6 Monster '''
        if self.direction == 0:
            self.image = pygame.transform.scale(pygame.image.\
                load('images/enemy1.png'), (48,48))
        else:
            self.image = pygame.transform.flip(pygame.transform.scale(\
                pygame.image.load('images/enemy1.png'), (48,48)),True,False)
        self.width,self.height = self.image.get_size()
        super(Enemy1, self).__init__(x,y)

    def update(self, screenWidth, screenHeight):
        #either moves left or right
        if self.direction == 0:
            self.x += 1
        else:
            self.x -= 1
        #moves down
        self.y += 3

        super(Enemy, self).update(screenWidth, screenHeight)

    def fireBullet(self):
        #fires a bullet sprite
        self.bullets.add(Enemy1BulletMid(self.x,self.y,self.bulletSize))
        self.bullets.add(Enemy1BulletLeft(self.x,self.y,self.bulletSize))
        self.bullets.add(Enemy1BulletRight(self.x,self.y,self.bulletSize))

class Enemy2(Enemy):

    def __init__(self,x,y):
        self.size = 30
        self.score = 200
        self.color = (0,255,0)
        self.health = 75
        self.bulletSize = 30
        self.images = []
        self.appendImages()
        self.index = 0
        self.image = pygame.transform.scale(self.images\
            [self.index].convert_alpha(),(64,64))
        self.width,self.height = self.image.get_size()
        super(Enemy2, self).__init__(x,y)

    def appendImages(self):

        ''' The source of the images is a gif file from \
        http://vignette3.wikia.nocookie.net/metalslug/images/d/d5/\
        Kraken.gif/revision/latest?cb=20100217144102'''

        self.images.append(pygame.image.load('images/enemy2_gif_files/1.gif'))
        self.images.append(pygame.image.load('images/enemy2_gif_files/2.gif'))
        self.images.append(pygame.image.load('images/enemy2_gif_files/3.gif'))
        self.images.append(pygame.image.load('images/enemy2_gif_files/4.gif'))

    def update(self, screenWidth, screenHeight):
        #enemy moves straight down and is animated
        self.y += 1
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = pygame.transform.scale(self.images\
            [self.index].convert_alpha(),(64,64))

        super(Enemy, self).update(screenWidth, screenHeight)

    def fireBullet(self):
        #fires a bullet sprite in 360 direction
        for i in range(0,12):
            self.bullets.add(Enemy2Bullet(self.x,self.y,self.bulletSize,\
                i*math.pi/6))

class Enemy3(Enemy):

    def __init__(self,x,y, movingRight):
        self.size = 25
        self.score = 200
        self.color = (255,165,0)
        self.health = 25
        self.bulletSize = 10
        self.images = []
        self.appendImages()
        self.index = 0
        self.image = pygame.transform.scale(self.images\
            [self.index], (144,48))
        self.width,self.height = self.image.get_size()
        #enemy moves to the right or left
        self.movingRight = movingRight
        super(Enemy3, self).__init__(x,y)

    def appendImages(self):

        ''' The source of the images is a gif file from \
        http://vignette3.wikia.nocookie.net/metalslug/images/7/70/\
        Vechiclesuper_21.gif/revision/latest?cb=20100422061120'''

        self.images.append(pygame.image.load('images/enemy3_gif_files/1.gif'))
        self.images.append(pygame.image.load('images/enemy3_gif_files/2.gif'))
        self.images.append(pygame.image.load('images/enemy3_gif_files/3.gif'))
        self.images.append(pygame.image.load('images/enemy3_gif_files/4.gif'))
        self.images.append(pygame.image.load('images/enemy3_gif_files/5.gif'))
        self.images.append(pygame.image.load('images/enemy3_gif_files/6.gif'))
        self.images.append(pygame.image.load('images/enemy3_gif_files/7.gif'))
        self.images.append(pygame.image.load('images/enemy3_gif_files/8.gif'))
        self.images.append(pygame.image.load('images/enemy3_gif_files/9.gif'))
        self.images.append(pygame.image.load('images/enemy3_gif_files/10.gif'))
        self.images.append(pygame.image.load('images/enemy3_gif_files/11.gif'))
        self.images.append(pygame.image.load('images/enemy3_gif_files/12.gif'))
        self.images.append(pygame.image.load('images/enemy3_gif_files/13.gif'))
        self.images.append(pygame.image.load('images/enemy3_gif_files/14.gif'))
        self.images.append(pygame.image.load('images/enemy3_gif_files/15.gif'))
        self.images.append(pygame.image.load('images/enemy3_gif_files/16.gif'))
        self.images.append(pygame.image.load('images/enemy3_gif_files/17.gif'))
        

    def update(self, screenWidth, screenHeight):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        #moves right
        if self.movingRight == True:
            self.image = pygame.transform.scale(self.images\
                [self.index],(144,48))
            self.x += 3
            #if the enemy hits the right edge of the screen it moves left
            if self.x > screenWidth:
                self.movingRight = False
        #moves left
        else:
            self.image = pygame.transform.flip(pygame.transform.scale(\
                self.images[self.index],(144,48)),True, False)
            self.x -= 3
            #reverses direction if hits left side of screen
            if self.x < 0:
                self.movingRight = True
        #slowly moves down
        self.y += 1
        super(Enemy, self).update(screenWidth, screenHeight)

    def fireBullet(self, playerX, playerY):
        #fires a bullet at player sprite
        if self.movingRight == True:
            x = self.x + 40
        else:
            x = self.x - 40
        if playerY > self.y+100:
            self.bullets.add(Enemy3Bullet(x,self.y,self.bulletSize,\
                playerX, playerY))

    def getEnemyBounds(self):
        #changes depending on if moving right or left rocket trail not in bound
        if self.movingRight == True:
            #gets bounds of bullet
            (x0, y0) = (self.x + 20, self.y-self.height/2)
            (x1, y1) = (self.x + self.width/2, self.y + self.height/2)
            return (x0, y0, x1, y1)
        else:
            #gets bounds of bullet
            (x0, y0) = (self.x - self.width/2, self.y-self.height/2)
            (x1, y1) = (self.x -20, self.y + self.height/2)
            return (x0, y0, x1, y1)

class Boss(Enemy):
    def __init__(self,x,y):
        #score from killing the boss
        self.score = 5000
        #how much health the boss has
        self.health = 1000
        #details of different bullets
        self.bullet1Size = 10
        self.bullet2Size = 10
        self.bullet3Size = 5
        self.bullet4Size = 41
        self.bullet1Timer = 5
        self.bullet2Timer = 10
        self.bullet3Timer = 30
        self.bullet4Timer = 20
        self.movingRight = True
        #data for boss blitzMode
        self.blitzMode = 0
        self.blitzed = False
        self.direction = 0
        #change in angle for spiral bullets
        self.delta = 0
        #Animates boss with numerous images
        self.images = []
        self.appendImages()
        self.index = 0
        self.image = pygame.transform.scale(self.images\
            [self.index], (224,120))
        self.width,self.height = self.image.get_size()
        super(Boss, self).__init__(x,y)

    def appendImages(self):

        ''' The source of the images is a gif file from \
        http://i698.photobucket.com/albums/vv350/kappakappa/Keesiii2.gif\
        This is an enemy from a Metal Slug game'''

        self.images.append(pygame.image.load('images/boss_gif_files/1.gif'))
        self.images.append(pygame.image.load('images/boss_gif_files/2.gif'))
        self.images.append(pygame.image.load('images/boss_gif_files/3.gif'))
        self.images.append(pygame.image.load('images/boss_gif_files/4.gif'))
        self.images.append(pygame.image.load('images/boss_gif_files/5.gif'))
        self.images.append(pygame.image.load('images/boss_gif_files/6.gif'))
        self.images.append(pygame.image.load('images/boss_gif_files/7.gif'))
        self.images.append(pygame.image.load('images/boss_gif_files/8.gif'))
        self.images.append(pygame.image.load('images/boss_gif_files/9.gif'))
        self.images.append(pygame.image.load('images/boss_gif_files/10.gif'))
        self.images.append(pygame.image.load('images/boss_gif_files/11.gif'))
        self.images.append(pygame.image.load('images/boss_gif_files/12.gif'))

    def update(self, screenWidth, screenHeight):
        if self.blitzMode > 0:
            #blitzMode only happens once
            self.blitzed = True
            if self.blitzMode > 200:
                self.blitzMode = -1
                self.x = screenWidth/2
                self.y = 60
            # Boss moves fast to hit player. Idea from Andy Shen.
            if self.blitzMode == 1:
                self.direction = 1
            if self.direction == 0:
                #comes from a random direction
                self.direction = random.randint(1,4)
                if self.direction == 1:
                    if self.blitzMode != 1:
                        self.x = random.randint(20,screenWidth-20)
                        self.y = 0
                elif self.direction == 2:
                    self.x = 0
                    self.y = random.randint(20,screenHeight-20)
                elif self.direction == 3:
                    self.y = screenHeight
                    self.x = random.randint(20,screenWidth-20)
                elif self.direction == 4:
                    self.x = screenWidth
                    self.y = random.randint(20,screenHeight-20)
            #moves fast in a random direction across the screen
            if self.direction == 1:
                self.y += 30
                if self.y > screenHeight:
                    self.direction = 0
            if self.direction == 2:
                self.x += 30
                if self.x > screenWidth:
                    self.direction = 0
            if self.direction == 3:
                self.y -= 30
                if self.y < 0:
                    self.direction = 0
            if self.direction == 4:
                self.x -= 30
                if self.x < 0:
                    self.direction = 0
            self.blitzMode += 1
                    
        elif self.health < 700 and self.blitzMode == 0:
            #moves right
            if self.movingRight == True:
                self.x += 3
                #if the enemy hits the right edge of the screen it moves left
                if self.x + 112 > screenWidth:
                    self.movingRight = False
            #moves left
            else:
                self.x -= 3
                #reverses direction if hits left side of screen
                if self.x - 112 < 0:
                    self.movingRight = True
        #switches through the images to animate the boss
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0 
        self.image = pygame.transform.scale(self.images\
            [self.index].convert_alpha(), (224,120))

        super(Enemy, self).update(screenWidth, screenHeight)

    def fireBullet1(self):
        self.delta += 4
        #fires a bullet sprite in spiral
        for i in range(0,8):
            self.bullets.add(BossBullet1(self.x,self.y,self.bullet1Size,\
                i*math.pi/4, self.delta))

    def fireBullet2(self):
        #first type of boss bullet
        for dx in [-3, -2, -1, 0, 1, 2, 3]:
            self.bullets.add(BossBullet2(self.x,self.y,self.bullet2Size,\
                dx))

    def fireBullet3(self):
        #fires a bullet sprite in 360 direction
        for i in range(0,12):
            self.bullets.add(BossBullet3(self.x,self.y,self.bullet3Size,\
                i*math.pi/6))

    def fireBullet4(self):
        #fires a bullet down that splits into other bullets
        self.bullets.add(BossBullet4(self.x, self.y, self.bullet4Size,
            math.pi/2, 2))