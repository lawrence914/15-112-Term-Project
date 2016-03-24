import pygame
import random
import eztext
import os
import sys
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep

'''
PygameGame Framework is created by Lukas Peraza
for 15-112 F15 Pygame Optional Lecture, 11/11/15
'''

from Player import Player
from Bullet import Bullet
from Bullet import PlayerBullet1
from Bullet import PlayerBullet2
from Bullet import PlayerBullet3
from Bullet import Enemy1BulletMid
from Bullet import Enemy1BulletLeft
from Bullet import Enemy1BulletRight
from Bullet import Enemy2Bullet
from Bullet import Enemy3Bullet
from Bullet import BossBullet1
from Bullet import BossBullet2
from Bullet import BossBullet3
from Bullet import BossBullet4
from Enemy import Enemy1
from Enemy import Enemy2
from Enemy import Enemy3
from Enemy import Boss
from Powerup import Bombup
from Powerup import Lifeup
from Powerup import Weaponup
from Explosion import Explosion
from Cloud import Cloud1
from Cloud import Cloud2
from Cloud import Cloud3
from Cloud import Cloud4

#Adapted from https://github.com/JRock007/boxxy/tree/master
def textInput(screen, maxLength, prompt):
    # defining some colors
    blue = (0, 0, 255)
    green = (0, 255, 0)
    red = (255, 0, 0)
    white = (255, 255, 255)
    black = (0, 0, 0)
    # fill the screen w/ black
    screen.fill(black)
    xpos = 250
    ypos = 100
    deltay = 25
    txtbx = []
    # For getting the return values
    a = ['']
    # here is the magic: making the text input
    # create an input with a max length of 45,
    # and a red color and a prompt saying 'type here $i: '
    txtbx.append(eztext.Input(maxlength=maxLength,
                              color=blue, x=xpos, y=ypos,
                              prompt=prompt))
    ypos += deltay

    # create the pygame clock
    clock = pygame.time.Clock()
    # main loop!

    while True:
        # make sure the program is running at 60 fps
        clock.tick(60)

        # events for txtbx
        events = pygame.event.get()
        for event in events:
            # close it x button is pressed
            if event.type == pygame.QUIT:
                return "None"

        # clear the screen
        screen.fill(white)  # I like black better :)
        # update txtbx and get return val
        a[0] = txtbx[0].update(events)
        txtbx[0].focus = True
        txtbx[0].color = black

        # blit txtbx[i] on the screen
        txtbx[0].draw(screen)

        # Changing the focus to the next element
        # every time enter is pressed
        if a[0] != None:
            return a[0]

        # refresh the display
        pygame.display.flip()

class TermProject(ConnectionListener):

    #adapted from https://github.com/JRock007/boxxy/tree/master
    def Network_startgame(self, data):
        self.running = True
        self.num = data["player"]
        self.gameid = data["gameid"]
        pygame.mixer.music.play(5,7)

    def Network_close(self, data):
        sys.exit()

    def init(self):
        pygame.init()
        player1 = Player(self.width / 4, self.height / 2, 0)
        player2 = Player(3*self.width / 4, self.height / 2, 1)
        self.player1Group = pygame.sprite.Group(player1)
        self.player2Group = pygame.sprite.Group(player2)
        self.enemy1Group = pygame.sprite.Group()
        self.enemy2Group = pygame.sprite.Group()
        self.enemy3Group = pygame.sprite.Group()
        self.bossGroup = pygame.sprite.Group()
        self.enemyBulletsGroup = pygame.sprite.Group()
        self.totalScore = 0
        self.bombAnimationTimer = -1
        self.bombupGroup = pygame.sprite.Group()
        self.lifeupGroup = pygame.sprite.Group()
        self.weaponupGroup = pygame.sprite.Group()
        self.explosionsGroup = pygame.sprite.Group()
        self.cloudsGroup = pygame.sprite.Group()
        #is the game over?
        self.isGameOver = False
        #did you win?
        self.gameWon = False
        self.player1Lives = 3
        self.player2Lives = 3
        self.player1Bombs = 3
        self.player2Bombs = 3
        self.player1Power = 1
        self.player2Power = 1
        self.player1WeaponLevel = 1
        self.player2WeaponLevel = 1
        #Server-Based Multiplayer
        self.running=False
        #background clouds
        self.makeClouds()
        #initializes sounds
        ''' Sounds are from timgormly's 8-bit sound package on Freesound
        https://freesound.org/people/timgormly/packs/10094/?page=1#sound'''
        self.hitSound = pygame.mixer.Sound('sounds/hit.ogg')
        self.fireSound = pygame.mixer.Sound('sounds/laser.ogg')
        self.bombupSound = pygame.mixer.Sound('sounds/bombup.ogg')
        self.lifeupSound = pygame.mixer.Sound('sounds/lifeup.ogg')
        self.weaponupSound = pygame.mixer.Sound('sounds/weaponup.ogg')
        self.playerHitSound = pygame.mixer.Sound('sounds/playerHit.ogg')
        ''' Explosion sound from\
        https://freesound.org/people/dkmedic/sounds/104439/'''
        self.explodeSound = pygame.mixer.Sound('sounds/explosion.wav')
        ''' Sound for using a bomb is from\
        https://freesound.org/people/CGEffex/sounds/93846/'''
        self.bombUseSound = pygame.mixer.Sound('sounds/bombUse.ogg')
        self.fireSound.set_volume(0.05)
        self.hitSound.set_volume(0.3)
        self.explodeSound.set_volume(1.0)
        #Game Music is Instrumental Core - Battlefield Main Theme
        pygame.mixer.music.load('sounds/gameMusic.ogg')
        #changes mouse for game purposes
        self.mouseImages = []
        self.mouseImagesAppend()
        self.mouseImageIndex = 0
        self.mouseImage = pygame.transform.scale(self.mouseImages\
            [self.mouseImageIndex].convert_alpha(),(24,24))

    def makeClouds(self):
        #this doesn't change depending on the server and remains the same every gmae
        cloud1 = Cloud1(100, 500)
        cloud2 = Cloud3(150, 30)
        cloud3 = Cloud2(300, 280)
        cloud4 = Cloud4(20, 370)
        cloud5 = Cloud4(420, 60)
        cloud6 = Cloud3(220, 170)
        cloud7 = Cloud2(390, 430)
        cloud8 = Cloud1(280, 620)
        self.cloudGroup = pygame.sprite.Group()
        self.cloudGroup.add(cloud1)
        self.cloudGroup.add(cloud2)
        self.cloudGroup.add(cloud3)
        self.cloudGroup.add(cloud4)
        self.cloudGroup.add(cloud5)
        self.cloudGroup.add(cloud6)
        self.cloudGroup.add(cloud7)
        self.cloudGroup.add(cloud8)

    def mouseImagesAppend(self):
        '''Images from http://www.rw-designer.com/cursor-view/81839.gif'''
        self.mouseImages.append(pygame.image.load('images/mouse_gif_files/1.gif'))
        self.mouseImages.append(pygame.image.load('images/mouse_gif_files/2.gif'))
        self.mouseImages.append(pygame.image.load('images/mouse_gif_files/3.gif'))
        self.mouseImages.append(pygame.image.load('images/mouse_gif_files/4.gif'))
        self.mouseImages.append(pygame.image.load('images/mouse_gif_files/5.gif'))
        self.mouseImages.append(pygame.image.load('images/mouse_gif_files/6.gif'))
        self.mouseImages.append(pygame.image.load('images/mouse_gif_files/7.gif'))
        self.mouseImages.append(pygame.image.load('images/mouse_gif_files/8.gif'))

    def Network_updateplayer1(self, data):
        #updates player 1 data
        if data["type"] == 1:
            player1 = Player(data["player1X"], data["player1Y"], 0)
            player1.index = data["player1Index"]
            player1.timer = data["player1Timer"]
            player1.countdown = data["player1Countdown"]
            player1.isHit = data["player1Hit"]
            self.player1Group = pygame.sprite.Group(player1)
            self.player1Group.update(self.width, self.height)
        #updates game data for player 1
        else:
            self.player1Lives = data["player1Lives"]
            self.player1Power = data["player1Power"]
            self.player1Bombs = data["player1Bombs"]
            self.player1WeaponLevel = data["player1Weapon"]

        self.redrawAll(self.screen)

    def Network_updateplayer2(self, data):
        #updates player 2 data
        if data["type"] == 1:
            player2 = Player(data["player2X"], data["player2Y"], 1)
            player2.index = data["player2Index"]
            player2.timer = data["player2Timer"]
            player2.countdown = data["player2Countdown"]
            player2.isHit = data["player2Hit"]
            self.player2Group = pygame.sprite.Group(player2)
            self.player2Group.update(self.width, self.height)
        #updates game data for player 2
        else:
            self.player2Lives = data["player2Lives"]
            self.player2Power = data["player2Power"]
            self.player2Bombs = data["player2Bombs"]
            self.player2WeaponLevel = data["player2Weapon"]
        
        self.redrawAll(self.screen)

    def Network_updatePlayerBullets(self, data):
        #updates player bullets
        if data["player"] == 1:
            player = self.player1Group.sprites()[0]
            weaponLevel = self.player1WeaponLevel
        else:
            player = self.player2Group.sprites()[0]
            weaponLevel = self.player2WeaponLevel
        if weaponLevel == 1:
            player.bullets.add(PlayerBullet1(data["x"],data["y"],data["size"]))
        elif weaponLevel == 2:
            player.bullets.add(PlayerBullet2(data["x"],data["y"],data["size"]))
        elif weaponLevel == 3:
            player.bullets.add(PlayerBullet3(data["x"],data["y"],data["size"]))

    def Network_updateEnemies(self, data):
        #updates enemy 1 on client
        if data["enemyType"] == 1:
            enemy = Enemy1(data["x"],data["y"],data["direction"])
            self.enemy1Group.add(enemy)
            enemy.bulletTimer = data["bulletTimer"]
            self.enemy1Group.update(self.width, self.height)
        #updates enemy 2 on client
        elif data["enemyType"] == 2:
            enemy = Enemy2(data["x"],data["y"])
            self.enemy2Group.add(enemy)
            enemy.bulletTimer = data["bulletTimer"]
            enemy.index = data["index"]
            self.enemy2Group.update(self.width, self.height)
        #updates enemy 3 on client
        elif data["enemyType"] == 3:
            enemy = Enemy3(data["x"],data["y"],data["movingRight"])
            self.enemy3Group.add(enemy)
            enemy.bulletTimer = data["bulletTimer"]
            enemy.index = data["index"]
            self.enemy3Group.update(self.width, self.height)
        #updates boss on client
        elif data["enemyType"] == 4:
            enemy = Boss(data["x"],data["y"])
            enemy.bullet1Timer = data["bullet1Timer"]
            enemy.bullet2Timer = data["bullet2Timer"]
            enemy.bullet3Timer = data["bullet3Timer"]
            enemy.movingRight = data["movingRight"]
            enemy.index = data["index"]
            enemy.delta = data["delta"]
            enemy.blitzMode = data["blitzMode"]
            enemy.blitzed = data["blitzed"]
            enemy.direction = data["direction"]
            self.bossGroup.add(enemy)
            self.bossGroup.update(self.width, self.height)
        enemy.health = data["health"]

    def Network_resetEnemies(self, data):
        #resets enemy groups so they don't stack
        self.enemy1Group = pygame.sprite.Group()
        self.enemy2Group = pygame.sprite.Group()
        self.enemy3Group = pygame.sprite.Group()
        self.bossGroup = pygame.sprite.Group()

    def Network_updateEnemy1Bullets(self, data):
        #updates different types of enemy1bullets
        if data["bulletType"] == 1:
            self.enemyBulletsGroup.add(Enemy1BulletMid(data["x"], \
                data["y"], data["size"]))
        if data["bulletType"] == 2:
            self.enemyBulletsGroup.add(Enemy1BulletLeft(data["x"], \
                data["y"], data["size"]))
        if data["bulletType"] == 3:
            self.enemyBulletsGroup.add(Enemy1BulletRight(data["x"], \
                data["y"], data["size"]))

    def Network_updateEnemy2Bullets(self, data):
        #updates enemy2 bullets
        self.enemyBulletsGroup.add(Enemy2Bullet(data["x"], \
                data["y"], data["size"], data["angle"]))

    def Network_updateEnemy3Bullets(self, data):
        #updates enemy3 bullets
        bullet = Enemy3Bullet(data["x"], \
                data["y"], data["size"], 0, 0)
        self.enemyBulletsGroup.add(bullet)
        bullet.xDistance = data["xDistance"]
        bullet.yDistance = data["yDistance"]
        bullet.timesMove = data["timesMove"]
        bullet.xMoveInterval = data["xMoveInterval"]

    def Network_updateBossBullets(self, data):
        #updates four different boss bullets
        if data["bulletType"] == 1:
            self.enemyBulletsGroup.add(BossBullet1(data["x"], \
                data["y"], data["size"], data["angle"],\
                data["delta"]))
        if data["bulletType"] == 2:
            self.enemyBulletsGroup.add(BossBullet2(data["x"], \
                data["y"], data["size"], data["dx"]))
        if data["bulletType"] == 3:
            self.enemyBulletsGroup.add(BossBullet3(data["x"], \
                data["y"], data["size"], data["angle"]))
        if data["bulletType"] == 4:
            bullet = BossBullet4(data["x"], data["y"], data["size"], \
                data["angle"], data["speed"])
            self.enemyBulletsGroup.add(bullet)
            bullet.timer = data["timer"]

    def Network_resetBullets(self, data):
        #resets all enemy bullets
        self.enemyBulletsGroup = pygame.sprite.Group()

    def Network_updatePowerups(self, data):
        #updates bombup
        if data["type"] == 1:
            bombup = Bombup(data["x"], data["y"])
            self.bombupGroup.add(bombup)
            bombup.timer = data["timer"]
        #updates lifeup
        if data["type"] == 2:
            lifeup = Lifeup(data["x"], data["y"])
            self.lifeupGroup.add(lifeup)
            lifeup.timer = data["timer"]
        #updates weaponup
        if data["type"] == 3:
            weaponup = Weaponup(data["x"], data["y"])
            self.weaponupGroup.add(weaponup)
            weaponup.timer = data["timer"]

    def Network_resetPowerups(self, data):
        #resets powerup groups
        self.bombupGroup = pygame.sprite.Group()
        self.lifeupGroup = pygame.sprite.Group()
        self.weaponupGroup = pygame.sprite.Group()

    def Network_updateExplosions(self, data):
        #updates the explosion animation
        explosion = Explosion(data["x"], data["y"],\
            data["width"], data["height"])
        self.explosionsGroup.add(explosion)
        explosion.index = data["index"]
        self.explosionsGroup.update(self.width, self.height)

    def Network_resetExplosions(self, data):
        #resets explosions group
        self.explosionsGroup = pygame.sprite.Group()

    def Network_updateGameInfo(self, data):
        #updates game info on client
        self.totalScore = data["score"]
        self.isGameOver = data["gameover"]
        self.gameWon = data["gamewon"]
        self.bombAnimationTimer = data["bombanimation"]

    #plays different sounds
    def Network_playHitSound(self, data):
        self.hitSound.play()

    def Network_playBombupSound(self, data):
        self.bombupSound.play()

    def Network_playLifeupSound(self, data):
        self.lifeupSound.play()

    def Network_playWeaponupSound(self, data):
        self.weaponupSound.play()

    def Network_playFireSound(self, data):
        self.fireSound.play()

    def Network_playPlayerHitSound(self, data):
        self.playerHitSound.play()

    def Network_playExplodeSound(self, data):
        self.explodeSound.play()

    def Network_playBombUseSound(self, data):
        self.bombUseSound.play()

    def mousePressedLeft(self, x, y):
        #fires when mouse is pressed
        self.Send({"action": "shoot", "num": self.num, "gameid": self.gameid})

    def mousePressedRight(self, x, y):
        #uses a bomb when right mouse button is pressed
        self.Send({"action": "usebomb", "num": self.num, "gameid": self.gameid})

    def mouseReleased(self, x, y):
        #stops firing when mouse is released
        self.Send({"action": "shoot", "num": self.num, "gameid": self.gameid})

    def mouseMotion(self, x, y):
        #moves player
        (x,y) = pygame.mouse.get_pos()
        self.Send({"action": "move", "x": x, "y": y, "num": self.num, "gameid": self.gameid})

    def mouseDrag(self, x, y):
        #can move player while firing
        (x,y) = pygame.mouse.get_pos()
        self.Send({"action": "move", "x": x, "y": y, "num": self.num, "gameid": self.gameid})

    def keyPressed(self, keyCode, modifier):
        #inputs key presses and sends data to server
        self.Send({"action": "keypressed", "keyCode": keyCode, "num": self.num, "gameid": self.gameid})

    def keyReleased(self, keyCode, modifier):
        self.Send({"action": "keyreleased", "keyCode": keyCode, "num": self.num, "gameid": self.gameid})

    def cloudEvent(self):
        #clouds move down and wrap around
        for cloud in self.cloudGroup:
            cloud.move(self.height)
        self.cloudGroup.update(self.width, self.height)

    def timerFired(self, time):
        #updates the connection and cloud event
        self.cloudEvent()
        connection.Pump()
        self.Pump()
        self.redrawAll(self.screen)

    def drawEnemies(self, screen):
        #draws all 3 enemy types
        self.enemy1Group.draw(screen)
        for enemy1 in self.enemy1Group:
            enemy1.bullets.draw(screen)
        self.enemy2Group.draw(screen)
        for enemy2 in self.enemy2Group:
            enemy2.bullets.draw(screen)
        self.enemy3Group.draw(screen)
        for enemy3 in self.enemy3Group:
            enemy3.bullets.draw(screen)
        self.bossGroup.draw(screen)
        for boss in self.bossGroup:
            boss.bullets.draw(screen)
            #draws boss health
            bossFont = pygame.font.Font("Audiowide.ttf", 14, bold=True)
            bossMessage = bossFont.render("Boss: ",\
             1, (0,0,0))
            screen.blit(bossMessage, (15, 10))
            pygame.draw.rect(screen,(255,0,0),((60,10),\
                (int(boss.health/10),15)))
        self.enemyBulletsGroup.draw(screen)

    def drawPowerups(self, screen):
        #the powerups flash when they are about to disappear
        for bombup in self.bombupGroup:
            if bombup.timer < 100:
                self.bombupGroup.draw(screen)
            elif bombup.timer >= 100 and bombup.timer % 2 == 0:
                self.bombupGroup.draw(screen)
        for lifeup in self.lifeupGroup:
            if lifeup.timer < 100:
                self.lifeupGroup.draw(screen)
            elif lifeup.timer >= 100 and lifeup.timer % 2 == 0:
                self.lifeupGroup.draw(screen)
        for weaponup in self.weaponupGroup:
            if weaponup.timer < 100:
                self.weaponupGroup.draw(screen)
            elif weaponup.timer >= 100 and weaponup.timer % 2 == 0:
                self.weaponupGroup.draw(screen)

    def drawPlayer1Details(self, screen):
        #tells you that its player 1
        player1Font = pygame.font.Font("Audiowide.ttf", 18, bold=True)
        player1Font.set_underline(1)
        player1Message = player1Font.render("Player 1",\
         1, (255,255,255))
        screen.blit(player1Message, (30, self.height - 110))
        #draws player1 power level on bottom right
        powerFont = pygame.font.Font("Audiowide.ttf", 14, bold=True)
        if self.player1Power < 3:
            powerMessage = powerFont.render("Power: %d" % self.player1Power,\
             1, (255,255,255))
        else:
            powerMessage = powerFont.render("Power: MAX",\
             1, (255,255,255))
        screen.blit(powerMessage, (30, self.height - 80))
        #draws the lives on bottom left
        livesFont = pygame.font.Font("Audiowide.ttf", 14, bold=True)
        livesMessage = livesFont.render("Lives: %d" % self.player1Lives,\
         1, (255,255,255))
        screen.blit(livesMessage, (30, self.height - 60))
        #draws the bombs on bottom left
        bombsFont = pygame.font.Font("Audiowide.ttf", 14, bold=True)
        bombsMessage = bombsFont.render("Bombs: %d" % self.player1Bombs,\
         1, (255,255,255))
        screen.blit(bombsMessage, (30, self.height - 40))

    def drawPlayer2Details(self, screen):
        #tells you that its player 1
        player2Font = pygame.font.Font("Audiowide.ttf", 18, bold=True)
        player2Font.set_underline(1)
        player2Message = player2Font.render("Player 2",\
         1, (255,255,255))
        screen.blit(player2Message, (self.width-90, self.height - 110))
        #draws the player power level on bottom left
        powerFont = pygame.font.Font("Audiowide.ttf", 14, bold=True)
        if self.player2Power < 3:
            powerMessage = powerFont.render("Power: %d" % self.player2Power,\
             1, (255,255,255))
        else:
            powerMessage = powerFont.render("Power: MAX",\
             1, (255,255,255))
        screen.blit(powerMessage, (self.width - 80, self.height - 80))
        #draws the lives on bottom left
        livesFont = pygame.font.Font("Audiowide.ttf", 14, bold=True)
        livesMessage = livesFont.render("Lives: %d" % self.player2Lives,\
         1, (255,255,255))
        screen.blit(livesMessage, (self.width - 80, self.height - 60))
        #draws the bombs on bottom left
        bombsFont = pygame.font.Font("Audiowide.ttf", 14, bold=True)
        bombsMessage = bombsFont.render("Bombs: %d" % self.player2Bombs,\
         1, (255,255,255))
        screen.blit(bombsMessage, (self.width - 80, self.height - 40))

    def drawTwoPlayerScreen(self, screen):
        #draws background clouds
        self.cloudGroup.draw(screen)
        #draws both players and their bullets
        if self.player1Lives > 0:
            if len(self.player1Group) > 0:
                player1 = self.player1Group.sprites()[0]
                player1.index
                if player1.countdown % 2 == 0:
                    self.player1Group.draw(screen)
                player1.bullets.draw(screen)
        if self.player2Lives > 0:
            if len(self.player2Group) > 0:
                player2 = self.player2Group.sprites()[0]
                if player2.countdown % 2 == 0:
                    self.player2Group.draw(screen)
                player2.bullets.draw(screen)
        #draws the enemies and powerups
        self.drawEnemies(screen)
        self.drawPowerups(screen)
        #draws explosions
        self.explosionsGroup.draw(screen)
        #draws the score on bottom right
        scoreFont = pygame.font.Font("Audiowide.ttf", 14, bold=True)
        scoreMessage = scoreFont.render("Score: %d" % self.totalScore,\
         1, (0,0,0))
        scorePos = scoreMessage.get_rect()
        scorePos.top = 30
        scorePos.right = self.width-10
        screen.blit(scoreMessage, scorePos)
        self.drawPlayer1Details(screen)
        self.drawPlayer2Details(screen)
        
    def drawGameOverScreen(self, screen):
        #draws game over screen
        gameOverFont = pygame.font.Font("Crushed.ttf", 40, bold=True)
        gameOver = gameOverFont.render("Game Over!", 1, (255,255,255))
        gameOverPos = gameOver.get_rect()
        gameOverPos.centerx = screen.get_size()[0]/2
        gameOverPos.centery = screen.get_size()[1]/2 - 60
        screen.blit(gameOver, gameOverPos)

        #score
        scoreFont = pygame.font.Font("Crushed.ttf", 20)
        score = scoreFont.render("Score: %d" % self.totalScore\
            , 1, (255,255,255))
        scorePos = score.get_rect()
        scorePos.centerx = screen.get_size()[0]/2
        scorePos.centery = screen.get_size()[1]/2
        screen.blit(score, scorePos)

        #restart game message
        restartFont = pygame.font.Font("Crushed.ttf", 13)
        restart = restartFont.render("Press Enter to Go Back to Main Menu"\
            , 1, (255,255,255))
        restartPos = restart.get_rect()
        restartPos.centerx = screen.get_size()[0]/2
        restartPos.centery = screen.get_size()[1]/2 + 225
        screen.blit(restart, restartPos)

    def drawGameWonScreen(self, screen):
        #draws game won screen
        gameWonFont = pygame.font.Font("Crushed.ttf", 40)
        gameWon = gameWonFont.render("You Win!", 1, (255,255,255))
        gameWonPos = gameWon.get_rect()
        gameWonPos.centerx = screen.get_size()[0]/2
        gameWonPos.centery = screen.get_size()[1]/2 - 20
        screen.blit(gameWon, gameWonPos)

        #score
        scoreFont = pygame.font.Font("Crushed.ttf", 20)
        score = scoreFont.render("Score: %d" % self.totalScore\
            , 1, (255,255,255))
        scorePos = score.get_rect()
        scorePos.centerx = screen.get_size()[0]/2
        scorePos.centery = screen.get_size()[1]/2
        screen.blit(score, scorePos)

        #restart game message
        restartFont = pygame.font.Font("Crushed.ttf", 13)
        restart = restartFont.render("Press Enter to Go Back to Main Menu"\
            , 1, (255,255,255))
        restartPos = restart.get_rect()
        restartPos.centerx = screen.get_size()[0]/2
        restartPos.centery = screen.get_size()[1]/2 + 20
        screen.blit(restart, restartPos)

    def redrawAll(self, screen):
        if self.isGameOver == False and self.gameWon == False:
            self.drawTwoPlayerScreen(screen)
            #draws bomb animation
            if self.bombAnimationTimer >= 0:
                if self.bombAnimationTimer % 5 == 0:
                    screen.fill((255,255,255))
        elif self.isGameOver == True:
            self.drawGameOverScreen(screen)
        else:
            self.drawGameWonScreen(screen)
        self.screen = screen

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=480, height=640, fps=180, title="Term Project"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        '''Background image is from 
        http://1.bp.blogspot.com/-iMMViPyVOnk/Ukr \
        iYf7srMI/AAAAAAAACJs/70U17vjatQI/s640/P1010098.jpg'''
        self.bg = pygame.image.load("images/bg.jpg")
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        self.screen = screen
        self.init()
        address = textInput(self.screen, 30, "Address of Server: ")
        try:
            if not address:
                host, port = "localhost", 8000
            else:
                host, port = address.split(":")
            self.Connect((host, int(port)))
        except:
            print("Error Connecting to Server")
            print("Usage:", "host:port")
            print("e.g.", "localhost:31425")
            sys.exit()

        print("Game client started, waiting for server and/or the other player")
        self.running = False
        self.owner = [[0 for x in range(6)] for y in range(6)]
        while not self.running:
            # events for txtbx
            events = pygame.event.get()
            # process other events
            for event in events:
                # close it x button is pressed
                if event.type == pygame.QUIT:
                    sys.exit()
            self.Pump()
            connection.Pump()
            sleep(0.05)
        print("Starting game")

    def run(self):
        clock = pygame.time.Clock()
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            pygame.event.pump()
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressedLeft(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.mousePressedRight(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            self.screen.blit(self.bg, (0, 0))
            if self.isGameOver == True:
                self.screen.fill((0,0,0))
            self.redrawAll(self.screen)
            pygame.display.flip()

        pygame.quit()

game = TermProject()
game.run()