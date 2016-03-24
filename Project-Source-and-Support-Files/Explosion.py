import pygame
import pyganim
import math
from GameSprite import GameSprite

class Explosion(GameSprite):

    def __init__(self,x,y, width, height):
        self.width = width
        self.height = height
        #enemy's bullet sprite group
        self.images = []
        self.appendImages()
        self.index = 0
        #scales the image down to match the size
        self.image = pygame.transform.scale(self.images\
            [self.index].convert_alpha(),(self.width+5,self.height+5))
        self.width,self.height = self.image.get_size()
        super(Explosion, self).__init__(x, y, self.image, self.width/2)
        self.updateRect()

    def appendImages(self):

        ''' The source of the images is a gif file from \
        https://media.giphy.com/media/9Hie5EMjkUURG/giphy.gif'''

        self.images.append(pygame.image.load(\
            'images/explosion_gif_files/1.gif'))
        self.images.append(pygame.image.load(\
            'images/explosion_gif_files/2.gif'))
        self.images.append(pygame.image.load(\
            'images/explosion_gif_files/3.gif'))
        self.images.append(pygame.image.load(\
            'images/explosion_gif_files/4.gif'))
        self.images.append(pygame.image.load(\
            'images/explosion_gif_files/5.gif'))
        self.images.append(pygame.image.load(\
            'images/explosion_gif_files/6.gif'))
        self.images.append(pygame.image.load(\
            'images/explosion_gif_files/7.gif'))
        self.images.append(pygame.image.load(\
            'images/explosion_gif_files/8.gif'))
        self.images.append(pygame.image.load(\
            'images/explosion_gif_files/9.gif'))
        self.images.append(pygame.image.load(\
            'images/explosion_gif_files/10.gif'))
        self.images.append(pygame.image.load(\
            'images/explosion_gif_files/11.gif'))
        self.images.append(pygame.image.load(\
            'images/explosion_gif_files/12.gif'))
        self.images.append(pygame.image.load(\
            'images/explosion_gif_files/13.gif'))
        self.images.append(pygame.image.load(\
            'images/explosion_gif_files/14.gif'))
        self.images.append(pygame.image.load\
            ('images/explosion_gif_files/15.gif'))
        self.images.append(pygame.image.load(\
            'images/explosion_gif_files/16.gif'))
        self.images.append(pygame.image.load(\
            'images/explosion_gif_files/17.gif'))
        self.images.append(pygame.image.load(\
            'images/explosion_gif_files/18.gif'))
        self.images.append(pygame.image.load(\
            'images/explosion_gif_files/19.gif'))
        

    def update(self, screenWidth, screenHeight):
        #runs explosion animation
        self.index += 1
        if self.index >= 18:
            self.index = 18
        self.image = pygame.transform.scale(self.images\
            [self.index],(self.width+5,self.height+5))
        self.updateRect()