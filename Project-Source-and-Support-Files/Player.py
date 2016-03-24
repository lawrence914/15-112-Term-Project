import pygame
from GameSprite import GameSprite
from Bullet import Bullet
from Bullet import PlayerBullet1
from Bullet import PlayerBullet2
from Bullet import PlayerBullet3

class Player(GameSprite):

    def __init__(self,x,y,number):
        #player's bullet sprite group
        self.bullets = pygame.sprite.Group()
        self.bulletSize = 10
        self.number = number
        #animates the player's sprite with numerous images
        self.images = []
        if number == 0:
            self.appendImages1()
        else:
            self.appendImages2()
        self.index = 0
        #scales the image down to match the size
        if number == 0:
            self.image = pygame.transform.scale(self.images\
                [self.index].convert_alpha(),(40,60))
        else:
            self.image = pygame.transform.scale(self.images\
                [self.index].convert_alpha(),(60,60))
        #animation timer
        self.timer = 0
        #invincibility after being hit
        self.countdown = 70
        self.isHit = False


        self.width,self.height = self.image.get_size()
        super(Player, self).__init__(x, y, self.image, self.height/2)

    def appendImages1(self):

        ''' The source of the images is a gif file from \
        http://vignette3.wikia.nocookie.net/dragons-crown/images/9/97/DC_-_\
        Wizard_Sprite.gif/revision/latest?cb=20130424094257'''

        self.images.append(pygame.image.load('images/player_gif_files/1.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/2.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/3.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/4.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/5.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/6.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/7.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/8.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/9.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/10.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/11.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/12.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/13.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/14.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/15.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/16.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/17.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/18.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/19.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/20.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/21.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/22.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/23.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/23.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/25.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/26.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/27.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/28.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/29.gif'))
        self.images.append(pygame.image.load('images/player_gif_files/30.gif'))

    def appendImages2(self):
        ''' The source of the images is a gif file from \
        http://img1.wikia.nocookie.net/__cb20130424094151/\
        dragons-crown/images/2/24/DC_-_Fighter_Sprite.gif'''

        self.images.append(pygame.image.load('images/player2_gif_files/1.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/2.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/3.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/4.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/5.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/6.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/7.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/8.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/9.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/10.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/11.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/12.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/13.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/14.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/15.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/16.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/17.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/18.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/19.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/20.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/21.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/22.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/23.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/23.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/25.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/26.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/27.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/28.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/29.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/30.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/31.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/32.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/33.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/34.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/35.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/36.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/37.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/38.gif'))
        self.images.append(pygame.image.load('images/player2_gif_files/39.gif'))

    def update(self, screenWidth, screenHeight):

        #slows down the animation to simulate flying
        if self.timer % 2 == 0:
            #updates image animation
            self.index += 1
        self.timer += 1
        if self.index >= len(self.images):
            self.index = 0
        if self.number == 0:
            self.image = pygame.transform.scale(self.images\
                [self.index].convert_alpha(),(40,60))
        else:
            self.image = pygame.transform.scale(self.images\
                [self.index].convert_alpha(),(60,60))
        if self.isHit == True:
            self.countdown -= 1
            if self.countdown == 0:
                self.isHit = False
                self.countdown = 100

        super(Player, self).update(screenWidth, screenHeight)

    def fireBullet(self, weaponLevel):
        #fires a bullet sprite
        if weaponLevel == 1:
            self.bullets.add(PlayerBullet1(self.x,self.y,self.bulletSize))
        elif weaponLevel == 2:
            #fires two bullets
            self.bullets.add(PlayerBullet2(self.x-5,self.y,self.bulletSize*2))
        elif weaponLevel == 3:
            #fires three bullets
            self.bullets.add(PlayerBullet3(self.x-10,self.y,self.bulletSize*2))

    def getPlayerBounds(self):
        #gets bounds of bullet
        (x0, y0) = (self.x-self.width/2, self.y-self.height/2)
        (x1, y1) = (self.x + self.width/2, self.y + self.height/2)
        return (x0, y0, x1, y1)