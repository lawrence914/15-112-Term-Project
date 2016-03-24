import pygame
from GameSprite import GameSprite

class Cloud(GameSprite):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 60

        super(Cloud, self).__init__(x, y, self.image, int(self.size) // 2)
        self.updateRect()

    def move(self, screenHeight):
        #clouds all move down slowly
        self.y += 1
        if self.y - 30 > screenHeight:
            self.y = -30 

class Cloud1(Cloud):

    def __init__(self, x, y):
        #cloud image
        '''Image from http://docs.garagegames.com/tgb/official/\
        content/documentation/Behavior Tutorials/images/\
        Rainy Day/cloud.png'''
        self.image = pygame.transform.scale(pygame.image.\
            load('images/cloud1.png'), (90,60))
        super(Cloud1, self).__init__(x, y)

class Cloud2(Cloud):

    def __init__(self, x, y):
        #cloud image
        '''Image from http://img07.deviantart.net/6d5f/i/2012/\
        005/c/e/cloud_close_png_by_digitalwideresource-d4ldq0t.png'''
        self.image = pygame.transform.scale(pygame.image.\
            load('images/cloud2.png'), (90,60))
        super(Cloud2, self).__init__(x, y)

class Cloud3(Cloud):
    
    def __init__(self, x, y):
        #cloud image
        '''Image from http://rain43.com/wp-content/themes/\
        june19-rain43/images/cloud-normal2.png'''
        self.image = pygame.transform.scale(pygame.image.\
            load('images/cloud3.png'), (90,60))
        super(Cloud3, self).__init__(x, y)

class Cloud4(Cloud):
    
    def __init__(self, x, y):
        #cloud image
        '''Image from http://img14.deviantart.net/8d74/i/2014\
        /139/7/5/cloud_png_version_2_by_thestockwarehouse-d7iz68k.png'''
        self.image = pygame.transform.scale(pygame.image.\
            load('images/cloud4.png'), (90,60))
        super(Cloud4, self).__init__(x, y)