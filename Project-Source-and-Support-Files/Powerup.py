import pygame
from pygame import gfxdraw
import math
from GameSprite import GameSprite

class Powerup(GameSprite):

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.timer = 0
        super(Powerup, self).__init__(x, y, self.image, self.size/2)
        self.updateRect()

    def getPowerupBounds(self):
        #gets bounds of bullet
        (x0, y0) = (self.x - self.size/2, self.y-(3**0.5)*self.size/2)
        (x1, y1) = (self.x + self.size/2, self.y)
        return (x0, y0, x1, y1)

class Bombup(Powerup):

    #gives player one more bomb
    def __init__(self,x,y):
        self.color = (255,255,0)
        self.size = 20
        ''' Image from
        http://www.yticamps.com/sbutler/Sprites/Maze%20-%20Platform/bomb.png'''
        self.image = pygame.transform.scale(pygame.image.\
            load('images/bombup.png'), (self.size,self.size))
        super(Bombup, self).__init__(x,y)
        
class Lifeup(Powerup):

    #gives player one more life
    def __init__(self,x,y):
        self.color = (255,0,255)
        self.size = 20
        ''' Image from
        http://www.yticamps.com/sbutler/Sprites/Maze%20-%20Platform/bomb.png'''
        self.image = pygame.transform.scale(pygame.image.\
            load('images/lifeup.png'), (self.size,self.size))
        super(Lifeup, self).__init__(x,y)

class Weaponup(Powerup):

    #strengthens the player's weapon
    def __init__(self,x,y):
        self.color = (0,255,255)
        self.size = 20
        ''' Image from
        http://www.yticamps.com/sbutler/Sprites/Maze%20-%20Platform/bomb.png'''
        self.image = pygame.transform.scale(pygame.image.\
            load('images/weaponup.png'), (self.size,self.size))
        super(Weaponup, self).__init__(x,y)