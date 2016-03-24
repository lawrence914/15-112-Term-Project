from __future__ import print_function, division
import pygame
import math
import pyganim
import random
from GameSprite import GameSprite

class Bullet(GameSprite):

    def __init__(self, x, y, size):
        #details of the bullet
        self.size = size

        super(Bullet, self).__init__(x, y, self.image, int(self.size) // 2)
        self.updateRect()

    def getBulletBounds(self):
        #gets bounds of bullet
        (x0, y0) = (self.x-self.size/2, self.y-self.size/2)
        (x1, y1) = (self.x + self.size/2, self.y + self.size/2)
        return (x0, y0, x1, y1)

class PlayerBullet(Bullet):

    def __init__(self, x, y, size):

        super(PlayerBullet, self).__init__(x, y, size)

    def move(self):
        #player bullet moves up
        self.y -= 15

class PlayerBullet1(PlayerBullet):

    def __init__(self, x, y, size):
        #bullet image
        '''Image from http://www.spriters-resource.com/\
        snes/ff5/sheet/56173/'''
        self.image = pygame.transform.scale(pygame.image.\
            load('images/playerBullet1.png'), (size*3,size*3))
        super(PlayerBullet1, self).__init__(x, y, size)

class PlayerBullet2(PlayerBullet):

    def __init__(self, x, y, size):
        #bullet image
        '''Image from http://www.spriters-resource.com/\
        snes/ff5/sheet/56173/'''
        self.image = pygame.transform.scale(pygame.image.\
            load('images/playerBullet2.png'), (size*2,size*2))
        super(PlayerBullet2, self).__init__(x, y, size)

class PlayerBullet3(PlayerBullet):

    def __init__(self, x, y, size):
        #bullet image
        '''Image from http://www.spriters-resource.com/\
        snes/ff5/sheet/56173/'''
        self.image = pygame.transform.scale(pygame.image.\
            load('images/playerBullet3.png'), (size*3,size*2))
        super(PlayerBullet3, self).__init__(x, y, size)

class Enemy1BulletMid(Bullet):

    def __init__(self, x, y, size):
        #bullet image
        '''Image from https://16bitjusticesociety.files.\
        wordpress.com/2010/11/bullet.png'''
        self.image = pygame.transform.scale(pygame.image.\
            load('images/enemy1Bullet.png'), (size*3,size*3))
        super(Enemy1BulletMid, self).__init__(x, y, size)

    def move(self):
        #Bullet moves straight down
        self.y += 5

class Enemy1BulletLeft(Bullet):

    def __init__(self, x, y, size):
        #bullet image
        '''Image from https://16bitjusticesociety.files.\
        wordpress.com/2010/11/bullet.png'''
        self.image = pygame.transform.scale(pygame.image.\
            load('images/enemy1Bullet.png'), (size*3,size*3))
        super(Enemy1BulletLeft, self).__init__(x, y, size)

    def move(self):
        #Bullet moves down and to the left
        self.y += 5
        self.x += 2

class Enemy1BulletRight(Bullet):

    def __init__(self, x, y, size):
        #bullet image
        '''Image from https://16bitjusticesociety.files.\
        wordpress.com/2010/11/bullet.png'''
        self.image = pygame.transform.scale(pygame.image.\
            load('images/enemy1Bullet.png'), (size*3,size*3))
        super(Enemy1BulletRight, self).__init__(x, y, size)

    def move(self):
        #Bullet moves down and to the right
        self.y += 5
        self.x -= 2

class Enemy2Bullet(Bullet):

    def __init__(self, x, y, size, angle):
        '''Image from http://cdn.sett.com/images/user/20140407/\
        ballidlefatty968be8477f76861b4ba5401d9a91dd19.gif'''
        self.image = pygame.transform.scale(pygame.image.\
            load('images/enemy2Bullet.gif'), (size*3,size*3))

        super(Enemy2Bullet, self).__init__(x, y, size)
        self.angle = angle

    def move(self):
        #Bullet moves in a direction depending on the angle
        self.x += 3*math.cos(self.angle)
        self.y += 3*math.sin(self.angle)

class Enemy3Bullet(Bullet):

    def __init__(self, x, y, size, playerX, playerY):
        '''Missile image from\
        http://s3.postimg.org/tomjxuuoj/Edited_Missile.png'''
        self.image = pygame.transform.rotate(pygame.transform.scale(\
            pygame.image.load('images/enemy3Bullet.png'), (size*3,size)),90)
        super(Enemy3Bullet, self).__init__(x, y, size)
        self.xDistance = self.x - playerX
        self.yDistance = self.y - playerY
        self.timesMove = self.yDistance/10
        self.xMoveInterval = self.xDistance/self.timesMove

    def move(self):
        #Bullet moves in a direction depending on the player's location
        if self.yDistance <= 0:
            self.y += 8
            self.x += self.xMoveInterval
        else:
            self.y -= 8
            self.x -= self.xMoveInterval

class BossBullet1(Bullet):

    #first type of boss bullet
    def __init__(self, x, y, size, angle, delta):
        #bullet image
        if delta % 12 == 0:
            '''Image from http://www.spriters-resource.com/\
            snes/ff5/sheet/56173/'''
            self.image = pygame.transform.scale(pygame.image.\
                load('images/bossBullet1Blue.png'), (size*3,size*3))
        elif delta % 12 == 4:
            '''Image from http://www.spriters-resource.com/\
            snes/ff5/sheet/56173/'''
            self.image = pygame.transform.scale(pygame.image.\
                load('images/bossBullet1Green.png'), (size*3,size*3))
        else:
            '''Image from http://www.spriters-resource.com/\
            snes/ff5/sheet/56173/'''
            self.image = pygame.transform.scale(pygame.image.\
                load('images/bossBullet1Yellow.png'), (size*3,size*3))
        super(BossBullet1, self).__init__(x, y, size)
        self.angle = angle
        self.delta = delta

    def move(self):
        #Bullet moves based on the angle. Ends up being a spiral of bullets.
        self.x += 3*math.cos(self.angle+self.delta)
        self.y += 3*math.sin(self.angle+self.delta)

class BossBullet2(Bullet):

    #second type of boss bullet
    def __init__(self, x, y, size, dx):
        '''Image from http://www.mariowiki.com/images/thumb/\
        c/c4/Fireball.JPG/200px-Fireball.JPG'''
        self.image = pygame.transform.scale(pygame.image.\
            load('images/bossBullet2.png'), (size*2,size*2))
        super(BossBullet2, self).__init__(x, y, size)
        self.dx = dx

    def move(self):
        #Bullet moves in a specified. Ends up as a cone of bullets
        self.x += self.dx
        self.y += 5

class BossBullet3(Bullet):

    #third type of boss bullet
    def __init__(self, x, y, size, angle):
        #bullet image
        '''Image from http://orig08.deviantart.net/1fe8/f/2011/244/b/6/\
        death_ball____frieeza_by_dbaf23-d48l1nc.gif'''
        self.image = pygame.transform.scale(pygame.image.\
            load('images/bossBullet3-1.gif'), (int(size*2),int(size*2)))
        super(BossBullet3, self).__init__(x, y, size)
        self.angle = angle

    def move(self):
        #Bullet moves depending on the angle. Ends up a circle that gets bigger
        self.x += 2*math.cos(self.angle)
        self.y += 2*math.sin(self.angle)
        self.size += .3
        self.__init__(self.x, self.y, self.size, self.angle)

class BossBullet4(Bullet):

    #fourth type of boss bullet
    def __init__(self, x, y, size, angle, speed):
        #bullet image
        '''Image from http://www.bogleech.com/\
        nbc/nbc-plasmaball.gif'''
        self.image = pygame.transform.scale(pygame.image.\
            load('images/bossBullet4.gif'), (size*2, size*2))
        super(BossBullet4, self).__init__(x, y, size)
        self.angle = angle
        self.speed = speed
        #splits at a random time
        self.timer = random.randint(35,60)

    def move(self):
        #Bullet splits into four smaller, faster ones at different angles
        self.x += self.speed*math.cos(self.angle)
        self.y += self.speed*math.sin(self.angle)
        self.timer -= 1