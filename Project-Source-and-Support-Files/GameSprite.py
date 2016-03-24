# This is a default object class that utilizes pygame's sprite features

import pygame

class GameSprite(pygame.sprite.Sprite):

    def __init__(self, x, y, image, radius):
        super(GameSprite, self).__init__()
        #position of the sprite
        self.x = x
        self.y = y
        #sprite image
        self.image = image
        self.radius = radius
        width, height = image.get_size()
        self.updateRect()

    def updateRect(self):
        width, height = self.image.get_size()
        self.width, self.height = width, height
        #updates rect attributes
        self.rect = pygame.Rect(self.x - width / 2, self.y - height / 2, \
            width, height)

    def update(self, screenWidth, screenHeight):
        self.updateRect()