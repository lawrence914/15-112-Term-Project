import PodSixNet.Channel
import PodSixNet.Server
import os
os.environ['PYGAME_FREETYPE'] = '1'
import pygame
import random
import math
from pygame.locals import *
from time import sleep
import eztext
import sys

#player object
from Player import Player
#various bullet objects
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
#enemy objects
from Enemy import Enemy
from Enemy import Enemy1
from Enemy import Enemy2
from Enemy import Enemy3
from Enemy import Boss
#powerup objects
from Powerup import Bombup
from Powerup import Lifeup
from Powerup import Weaponup
#explosion object
from Explosion import Explosion
#background cloud objects
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
    ypos = 25
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
        # make sure the program is running at 30 fps
        clock.tick(30)

        # events for txtbx
        events = pygame.event.get()
        # process other events
        for event in events:
            # close it x button si pressed
            if event.type == QUIT:
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

class ClientChannel(PodSixNet.Channel.Channel):
    def Network(self, data):
        pass
        # print(data)

    def Network_shoot(self, data):
        # player number (1 or 0)
        num = data["num"]

        # id of game given by server at start of game
        self.gameid = data["gameid"]

        # tells server to shoot
        self._server.playerShoot(data, num, self.gameid)

    def Network_move(self, data):
        num = data["num"]
        self.gameid = data["gameid"]
        #tells server to move the player
        self._server.playerMove(data, num, self.gameid)

    def Network_keypressed(self, data):
        num = data["num"]
        self.gameid = data["gameid"]
        #tells server to run keypressed
        self._server.keypressed(data, num, self.gameid)

    def Network_keyreleased(self, data):
        num = data["num"]
        self.gameid = data["gameid"]
        #tells server to run keyreleased
        self._server.keyreleased(data, num, self.gameid)

    def Network_usebomb(self, data):
        num = data["num"]
        self.gameid = data["gameid"]
        #tells server that player uses a bomb
        self._server.usebomb(data, num, self.gameid)

    def Close(self):
        self._server.close(self.gameid)

'''Adapted from https://github.com/JRock007/boxxy/tree/master
channelClass, init, Connected, close are from the github. 
Every other function was made by me'''
class GameServer(PodSixNet.Server.Server):

    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)
        self.games = []
        self.queue = None
        self.currentIndex = 0
        print("Waiting for clients...")

    def Connected(self, channel, addr):
        print("new connection:", channel)
        if self.queue is None:
            print("Player 1 joined the game !")
            self.currentIndex += 1
            channel.gameid = self.currentIndex
            # starts a game when the first player connects to the channel
            self.queue = Game(channel, self.currentIndex)
            self.queue.init()
        else:
            print("Player 2 joined the game !")
            channel.gameid = self.currentIndex
            self.queue.player2 = channel
            # when both players join, the game starts
            self.queue.player1.Send({"action": "startgame", "player": 0, \
                "gameid": self.queue.gameid})
            self.queue.player2.Send({"action": "startgame", "player": 1, \
                "gameid": self.queue.gameid})
            self.games.append(self.queue)
            self.queue = None

    def playerShoot(self, data, num, gameid):
        game = [a for a in self.games if a.gameid == gameid]
        if len(game) == 1:
            #tells game to shoot
            game[0].multiPlayerShoot(data, num)

    def playerMove(self, data, num, gameid):
        game = [a for a in self.games if a.gameid == gameid]
        if len(game) == 1:
            #tells game to move player
            game[0].multiPlayerMove(data, num)

    def keypressed(self, data, num, gameid):
        game = [a for a in self.games if a.gameid == gameid]
        if len(game) == 1:
            #tells game to check for key pressed
            game[0].multiKeyPressed(data, num)

    def keyreleased(self, data, num, gameid):
        game = [a for a in self.games if a.gameid == gameid]
        if len(game) == 1:
            #tells game to check for key released
            game[0].multiKeyReleased(data, num)

    def usebomb(self, data, num, gameid):
        game = [a for a in self.games if a.gameid == gameid]
        if len(game) == 1:
            #tells game to use a bomb
            game[0].multiUseBomb(data, num)

    def close(self, gameid):
        try:
            game = [a for a in self.games if a.gameid == gameid][0]
            game.player1.Send({"action": "close"})
            game.player2.Send({"action": "close"})
        except:
            pass

    def tick(self):
        #runs the game on the server and calls timer fired
        clock = pygame.time.Clock()
        for game in self.games:
            time = clock.tick(7)
            game.menuMode = False
            game.multiplayerMode = True
            game.gameStarted = True
            game.timerFired(time)
        self.Pump()

class Game:

    def init(self):
        pygame.init()
        #initializes player sprite
        player = Player(self.width / 2, self.height / 2, 0)
        self.playerGroup = pygame.sprite.Group(player)
        #checks to see if player is firing
        self.firing = False
        #checks to see if player is using ability to slow time
        self.abilityUsed = False
        #enemy groups and time intervals for appearance
        self.enemy1Group = pygame.sprite.Group()
        self.enemy1Timer = 1
        self.enemy2Group = pygame.sprite.Group()
        self.enemy2Timer = 300
        self.enemy3Group = pygame.sprite.Group()
        self.enemy3Timer = 500
        self.bossGroup = pygame.sprite.Group()
        self.bossTimer = 1000
        self.totalScore = 0
        #details for the player
        self.playerLives = 20
        self.playerBombs = 20
        self.bombUsed = False
        #player's power depends on enemies killed
        self.enemyKillCount = 0
        self.playerPower = 1 + self.enemyKillCount//10
        #weapon level defines columns of bullets
        self.playerWeaponLevel = 1
        self.bombAnimationTimer = -1
        #how much energy is available to use the slow time ability
        self.abilityGauge = 100
        self.abilityTimer = 0
        #powerup groups
        self.bombupGroup = pygame.sprite.Group()
        self.lifeupGroup = pygame.sprite.Group()
        self.weaponupGroup = pygame.sprite.Group()
        #is the game over?
        self.isGameOver = False
        #did you win?
        self.gameWon = False
        #Main Menu Mode
        self.menuMode = True
        #Instructions Page
        self.instructionsMode = False
        #High Scores Page
        self.highScoresMode = False
        #Single Player Game Mode
        self.gameMode1 = False
        #Two Player Game Mode
        self.gameMode2 = False
        #pause function
        self.isPaused = False
        #text box for player to input name
        self.textbox = eztext.Input(maxlength=45, color=(255,255,255), \
            prompt='Enter your name here: ')
        #Audiowide font was created by Astigmatic One Eye Typographic Institute
        textboxFont = pygame.font.Font("Audiowide.ttf", 14, bold=True)
        self.textbox.set_font(textboxFont)
        #checks to see if player is finished entering their name
        self.nameEnterDone = False
        #two player details
        self.firing1 = False
        self.firing2 = False
        self.player1Lives = 3
        self.player2Lives = 3
        self.player1Bombs = 3
        self.player2Bombs = 3
        self.player1EnemyKillCount = 0
        self.player2EnemyKillCount = 0
        self.player1Power = 1 + self.player1EnemyKillCount//10
        self.player2Power = 1 + self.player2EnemyKillCount//10
        self.player1WeaponLevel = 1
        self.player2WeaponLevel = 1
        #Server-Based Multiplayer
        self.multiplayerMode = False
        self.running = False
        self.gameStarted = False
        player1 = Player(self.width / 4, self.height / 2, 0)
        player2 = Player(3*self.width / 4, self.height / 2, 1)
        self.player1Group = pygame.sprite.Group(player1)
        self.player2Group = pygame.sprite.Group(player2)
        #explosions
        self.explosionGroup = pygame.sprite.Group()
        #background clouds
        self.makeClouds()
        #initializes sounds
        ''' Sounds are from timgormly's 8-bit sound package on Freesound
        https://freesound.org/people/timgormly/packs/10094/?page=1#sound'''
        pygame.mixer.init()
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
        #fixes volume for sounds
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
        #creates all of the background clouds in the game
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
        #images for animating the mouse cursor
        '''Images from http://www.rw-designer.com/cursor-view/81839.gif'''
        self.mouseImages.append(pygame.image.load(\
            'images/mouse_gif_files/1.gif'))
        self.mouseImages.append(pygame.image.load(\
            'images/mouse_gif_files/2.gif'))
        self.mouseImages.append(pygame.image.load(\
            'images/mouse_gif_files/3.gif'))
        self.mouseImages.append(pygame.image.load(\
            'images/mouse_gif_files/4.gif'))
        self.mouseImages.append(pygame.image.load(\
            'images/mouse_gif_files/5.gif'))
        self.mouseImages.append(pygame.image.load(\
            'images/mouse_gif_files/6.gif'))
        self.mouseImages.append(pygame.image.load(\
            'images/mouse_gif_files/7.gif'))
        self.mouseImages.append(pygame.image.load(\
            'images/mouse_gif_files/8.gif'))

    def mousePressedLeft(self, x, y):
        if self.gameMode1 == True:
            #fires when mouse is pressed
            self.firing = True
        elif self.gameMode2 == True:
            #player 1 is controlled with the mouse
            self.firing1 = True
        elif self.menuMode == True:
            (x, y) = pygame.mouse.get_pos()
            mouseBounds = (x,y,x,y)
            singlePlayerBounds = (140,200,340,260)
            twoPlayerBounds = (140,280,340,340)
            multiPlayerBounds = (140,360,340,420)
            instructionsBounds = (140,440,340,500)
            highScoresBounds = (140,520,340,580)
            #checks to see if you click on a menu button
            if self.boundsIntersect(mouseBounds, singlePlayerBounds):
                self.gameMode1 = True
                #single player mode starts
                player = Player(self.width / 2, self.height / 2, 0)
                self.playerGroup = pygame.sprite.Group(player)
                self.menuMode = False
                pygame.mixer.music.play(5,7)
            elif self.boundsIntersect(mouseBounds, twoPlayerBounds):
                self.gameMode2 = True
                #local two player mode starts
                player1 = Player(self.width / 4, self.height / 2, 0)
                player2 = Player(3*self.width / 4, self.height / 2, 1)
                self.player1Group = pygame.sprite.Group(player1)
                self.player2Group = pygame.sprite.Group(player2)
                self.menuMode = False
                pygame.mixer.music.play(5,7)
            elif self.boundsIntersect(mouseBounds, multiPlayerBounds):
                multiplayerMode = True
                #starts a server for server based multiplayer
                self.serverMode()
                self.gameStarted = True
                player1 = Player(self.width / 4, self.height / 2, 0)
                player2 = Player(3*self.width / 4, self.height / 2, 1)
                self.player1Group = pygame.sprite.Group(player1)
                self.player2Group = pygame.sprite.Group(player2)
                self.menuMode = False
                pygame.mixer.music.play(5,7)
            elif self.boundsIntersect(mouseBounds, instructionsBounds):
                self.instructionsMode = True
                #opens instructions page
                self.menuMode = False
            elif self.boundsIntersect(mouseBounds, highScoresBounds):
                self.highScoresMode = True
                #opens highscores page
                self.menuMode = False

    def serverMode(self):
        print("STARTING SERVER ON LOCALHOST")

        
        width, height = 500, 50
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Game Server")

        #  try:
        address = textInput(screen, 200, "Host:Port (localhost:8000): ")
        if address == "None":
            sys.exit()

        if not address:
            host, port = "localhost", 8000
        else:
            host, port = address.split(":")
        gameServe = GameServer(localaddr=(host, int(port)))
        while True:
            events = pygame.event.get()
            # process other events
            for event in events:
                # close it x button si pressed
                if event.type == QUIT:
                    sys.exit()

            gameServe.tick()
            sleep(0.01)

    def mousePressedRight(self, x, y):
        if self.isPaused == False:
            if self.gameMode1 == True:
                #uses bomb with right mouse click
                if self.playerBombs > 0:
                    self.bombUsed = True
                    self.playerBombs -= 1
            elif self.gameMode2 == True:
                #player 1 uses bomb with right mouse click
                if self.player1Bombs > 0:
                    self.bombUsed = True
                    self.player1Bombs -= 1

    def mouseReleased(self, x, y):
        if self.gameMode1 == True:
            self.firing = False
        elif self.gameMode2 == True:
            self.firing1 = False

    def mouseMotion(self, x, y):
        if self.isPaused == False:
            if self.gameMode1 == True:
                #moves player
                player = self.playerGroup.sprites()[0]
                (player.x,player.y) = pygame.mouse.get_pos()
            elif self.gameMode2 == True:
                #player 1 is moved by mouse
                if self.player1Lives > 0:
                    player1 = self.player1Group.sprites()[0]
                    (player1.x, player1.y) = pygame.mouse.get_pos()

    def mouseDrag(self, x, y):
        if self.isPaused == False:
            if self.gameMode1 == True:
                #can move player while firing
                player = self.playerGroup.sprites()[0]
                (player.x,player.y) = pygame.mouse.get_pos()
            elif self.gameMode2 == True:
                if self.player1Lives > 0:
                    player1 = self.player1Group.sprites()[0]
                    (player1.x, player1.y) = pygame.mouse.get_pos()

    def movePlayer(self, player):
        if self.isKeyPressed(pygame.K_LEFT):
            if player.x - player.width/2 > 0:
                player.x -= 10

        if self.isKeyPressed(pygame.K_RIGHT):
            if player.x + player.width/2 < self.width:
                player.x += 10

        if self.isKeyPressed(pygame.K_UP):
            if player.y - player.height/2 > 0:
                player.y -= 10

        if self.isKeyPressed(pygame.K_DOWN):
            if player.y + player.height/2 < self.height:
                player.y += 10

    def keyPressed(self, keyCode, modifier):
        #pauses the game
        if keyCode == pygame.K_p:
            if self.isPaused == False:
                self.isPaused = True
            else:
                self.isPaused = False
        if self.isPaused == False:
            if self.gameMode1 == True:
                player = self.playerGroup.sprites()[0]
                #spaces slows down time
                if keyCode == pygame.K_SPACE:
                    if self.abilityGauge > 0:
                        self.abilityUsed = True
                #so does the shift key
                elif keyCode == pygame.K_LSHIFT:
                    if self.abilityGauge > 0:
                        self.abilityUsed = True
                #alternative way of firing with z key
                elif keyCode == pygame.K_z:
                    self.firing = True
                #alternative way of using a bomb
                elif keyCode == pygame.K_x:
                    if self.playerBombs > 0:
                        self.bombUsed = True
                        self.playerBombs -= 1
                #skip to boss
                elif keyCode == pygame.K_b:
                    self.bossTimer = 1
                elif keyCode == pygame.K_ESCAPE:
                    self.init()
                if self.isGameOver == True or self.gameWon == True:
                    if keyCode == pygame.K_RETURN:
                        self.name = self.textbox.value
                        if len(self.name) > 0:
                            information = str(self.totalScore) + "/"+self.name
                            #appends name and score to a file
                            with open("file.txt", "a") as highscores_file:
                                highscores_file.write(information + "\n")
                        self.init()
            elif self.gameMode2 == True:
                #player 2 fires with z key
                if keyCode == pygame.K_z:
                    self.firing2 = True
                #player 2 uses bombs with x
                elif keyCode == pygame.K_x:
                    if self.player2Bombs > 0:
                        self.bombUsed = True
                        self.player2Bombs -= 1
                #skip to boss
                elif keyCode == pygame.K_b:
                    self.bossTimer = 1
                #pauses the game
                elif keyCode == pygame.K_p:
                    if self.isPaused == False:
                        self.isPaused = True
                    else:
                        self.isPaused = False
                elif keyCode == pygame.K_ESCAPE:
                    self.init()
                #no high scores for two player mode
                if self.isGameOver or self.gameWon == True:
                    if keyCode == pygame.K_RETURN:
                        self.init()
            elif self.instructionsMode == True or self.highScoresMode == True:
                if keyCode == pygame.K_BACKSPACE:
                    self.init()

    def keyReleased(self, keyCode, modifier):
        if self.gameMode1 == True:
            if keyCode == pygame.K_SPACE:
                self.abilityUsed = False
            elif keyCode == pygame.K_LSHIFT:
                self.abilityUsed = False
            elif keyCode == pygame.K_z:
                self.firing = False
        elif self.gameMode2 == True:
            if keyCode == pygame.K_z:
                self.firing2 = False

    #taken from side scroller
    def boundsIntersect(self, boundsA, boundsB):
        # return l2<=r1 and t2<=b1 and l1<=r2 and t1<=b2
        if boundsA != None and boundsB != None:
            (ax0, ay0, ax1, ay1) = boundsA
            (bx0, by0, bx1, by1) = boundsB
            return ((ax1 >= bx0) and (bx1 >= ax0) and
                    (ay1 >= by0) and (by1 >= ay0))

    def definePlayer(self, index):
        #defines a player based on index so functions can be repeatedly used
        player = None
        if self.gameMode1 == True:
            player = self.playerGroup.sprites()[index]
        elif self.gameMode2 == True or self.multiplayerMode == True:
            if index == 0:
                if self.player1Lives > 0:
                    player = self.player1Group.sprites()[0]
            else:
                if self.player2Lives > 0:
                    player = self.player2Group.sprites()[0]
        return player

    def hitEnemy1(self,bullet,index=0):
        player = self.definePlayer(index)
        bulletBounds = bullet.getBulletBounds()
        #checks to see if player bullets hit enemy1
        for enemy1 in self.enemy1Group:
            enemyBounds = enemy1.getEnemyBounds()
            if self.boundsIntersect(bulletBounds,enemyBounds):
                self.hitSound.play()
                if self.gameMode1 == True:
                    #enemy loses health
                    enemy1.health -= self.playerPower
                elif self.gameMode2 == True or self.multiplayerMode == True:
                    if self.multiplayerMode == True:
                        self.player1.Send({"action": "playHitSound"})
                        self.player2.Send({"action": "playHitSound"})
                    if index == 0:
                        enemy1.health -= self.player1Power
                    else:
                        enemy1.health -= self.player2Power
                #enemy dies if its health reaches 0
                if enemy1.health <= 0:
                    #chance for powerups to appear when enemy dies
                    self.powerupAppear(enemy1)
                    #makes an explosion when enemy dies
                    self.explosionGroup.add(Explosion(enemy1.x,\
                        enemy1.y, enemy1.width, enemy1.height))
                    enemy1.kill()
                    #plays an explosion sound
                    self.explodeSound.play()
                    #sends sound data to clients
                    if self.multiplayerMode == True:
                        self.player1.Send({"action": "playExplodeSound"})
                        self.player2.Send({"action": "playExplodeSound"})
                    self.enemyKillCount += 1
                    #adds the score of the hit enemy
                    self.totalScore += enemy1.score

                player.bullets.remove(bullet)

    def hitEnemy2(self,bullet,index=0):
        player = self.definePlayer(index)
        bulletBounds = bullet.getBulletBounds()
        #checks to see if player bullets hit enemy1
        for enemy2 in self.enemy2Group:
            enemyBounds = enemy2.getEnemyBounds()
            if self.boundsIntersect(bulletBounds,enemyBounds):
                self.hitSound.play()
                if self.gameMode1 == True:
                    #enemy loses health
                    enemy2.health -= self.playerPower
                elif self.gameMode2 == True or self.multiplayerMode == True:
                    if self.multiplayerMode == True:
                        self.player1.Send({"action": "playHitSound"})
                        self.player2.Send({"action": "playHitSound"})
                    if index == 0:
                        enemy2.health -= self.player1Power
                    else:
                        enemy2.health -= self.player2Power
                #enemy dies if its health reaches 0
                if enemy2.health <= 0:
                    #chance for powerups to appear when enemy dies
                    self.powerupAppear(enemy2)
                    self.explosionGroup.add(Explosion(enemy2.x,\
                        enemy2.y, enemy2.width, enemy2.height))
                    enemy2.kill()
                    self.explodeSound.play()
                    if self.multiplayerMode == True:
                        self.player1.Send({"action": "playExplodeSound"})
                        self.player2.Send({"action": "playExplodeSound"})
                    self.enemyKillCount += 1
                    #adds the score of the hit enemy
                    self.totalScore += enemy2.score

                player.bullets.remove(bullet)

    def hitEnemy3(self,bullet,index=0):
        player = self.definePlayer(index)
        bulletBounds = bullet.getBulletBounds()
        #checks to see if player bullets hit enemy1
        for enemy3 in self.enemy3Group:
            enemyBounds = enemy3.getEnemyBounds()
            if self.boundsIntersect(bulletBounds,enemyBounds):
                self.hitSound.play()
                if self.gameMode1 == True:
                    #enemy loses health
                    enemy3.health -= self.playerPower
                elif self.gameMode2 == True or self.multiplayerMode == True:
                    if self.multiplayerMode == True:
                        self.player1.Send({"action": "playHitSound"})
                        self.player2.Send({"action": "playHitSound"})
                    if index == 0:
                        enemy3.health -= self.player1Power
                    else:
                        enemy3.health -= self.player2Power
                #enemy dies if its health reaches 0
                if enemy3.health <= 0:
                    #chance for powerups to appear when enemy dies
                    self.powerupAppear(enemy3)
                    #centers the explosion on the enemy's body
                    if enemy3.movingRight == True:
                        self.explosionGroup.add(Explosion(enemy3.x+40,\
                            enemy3.y, 48, enemy3.height))
                    else:
                        self.explosionGroup.add(Explosion(enemy3.x-40,\
                            enemy3.y, 48, enemy3.height))
                    enemy3.kill()
                    self.explodeSound.play()
                    if self.multiplayerMode == True:
                        self.player1.Send({"action": "playExplodeSound"})
                        self.player2.Send({"action": "playExplodeSound"})
                    self.enemyKillCount += 1
                    #adds the score of the hit enemy
                    self.totalScore += enemy3.score

                player.bullets.remove(bullet)

    def hitBoss(self,bullet,index=0):
        player = self.definePlayer(index)
        bulletBounds = bullet.getBulletBounds()
        #checks to see if player bullets hit enemy1
        for boss in self.bossGroup:
            bossBounds = boss.getEnemyBounds()
            if self.boundsIntersect(bulletBounds,bossBounds):
                self.hitSound.play()
                if self.gameMode1 == True:
                    #enemy loses health
                    boss.health -= self.playerPower
                elif self.gameMode2 == True or self.multiplayerMode == True:
                    if self.multiplayerMode == True:
                        self.player1.Send({"action": "playHitSound"})
                        self.player2.Send({"action": "playHitSound"})
                    if index == 0:
                        boss.health -= self.player1Power
                    else:
                        boss.health -= self.player2Power
                #enemy dies if its health reaches 0
                if boss.health <= 0:
                    self.explosionGroup.add(Explosion(boss.x,\
                        boss.y, boss.width, boss.height))
                    boss.kill()
                    self.explodeSound.play()
                    if self.multiplayerMode == True:
                        self.player1.Send({"action": "playExplodeSound"})
                        self.player2.Send({"action": "playExplodeSound"})
                    #adds the score of the hit enemy
                    self.totalScore += boss.score
                    self.gameWon = True

                player.bullets.remove(bullet)

    def hitsPowerup(self,index=0):
        player = self.definePlayer(index)
        playerBounds = player.getPlayerBounds()
        #checks to see if player hits a bombup
        for bombup in self.bombupGroup:
            bombupBounds = bombup.getPowerupBounds()
            if self.boundsIntersect(playerBounds, bombupBounds):
                #plays sound for collecting a bombup
                self.bombupSound.play()
                #player's bombs increase by 1
                if self.gameMode1 == True:
                    self.playerBombs += 1
                elif self.gameMode2 == True or self.multiplayerMode == True:
                    if self.multiplayerMode == True:
                        self.player1.Send({"action": "playBombupSound"})
                        self.player2.Send({"action": "playBombupSound"})
                    if index == 0:
                        self.player1Bombs += 1
                    else:
                        self.player2Bombs += 1
                #deletes the bombup after a player gets it
                bombup.kill()
        #checks to see if player hits a lifeup
        for lifeup in self.lifeupGroup:
            lifeupBounds = lifeup.getPowerupBounds()
            if self.boundsIntersect(playerBounds, lifeupBounds):
                #plays sound for collecting a lifeup
                self.lifeupSound.play()
                #player's lives increase by 1
                if self.gameMode1 == True:
                    self.playerLives += 1
                elif self.gameMode2 == True or self.multiplayerMode == True:
                    if self.multiplayerMode == True:
                        self.player1.Send({"action": "playLifeupSound"})
                        self.player2.Send({"action": "playLifeupSound"})
                    if index == 0:
                        self.player1Lives += 1
                    else:
                        self.player2Lives += 1
                # deletes the lifeup after a player gets it
                lifeup.kill()
        #checks to see if player hits a weaponup
        for weaponup in self.weaponupGroup:
            weaponupBounds = weaponup.getPowerupBounds()
            if self.boundsIntersect(playerBounds, weaponupBounds):
                #plays the sound for collecting a weaponup
                self.weaponupSound.play()
                #player's weapon level increase by 1
                if self.gameMode1 == True:
                    if self.playerWeaponLevel < 3:
                        self.playerWeaponLevel += 1
                elif self.gameMode2 == True or self.multiplayerMode == True:
                    if self.multiplayerMode == True:
                        self.player1.Send({"action": "playWeaponupSound"})
                        self.player2.Send({"action": "playWeaponupSound"})
                    if index == 0:
                        if self.player1WeaponLevel < 3:
                            self.player1WeaponLevel += 1
                    else:
                        if self.player2WeaponLevel < 3:
                            self.player2WeaponLevel += 1
                #deletes weaponup when a player gets it
                weaponup.kill()

    def playerMovement(self,index=0):
        player = self.definePlayer(index)
        if self.gameMode1 == True:
            self.playerGroup.update(self.width, self.height)
            self.movePlayer(player)
            #fires bullets
            if self.firing == True:
                self.fireSound.play()
                player.fireBullet(self.playerWeaponLevel)
        elif self.gameMode2 == True or self.multiplayerMode == True:
            #checks if player 1 fires a bullet
            if index == 0:
                self.player1Group.update(self.width, self.height)
                if self.firing1 == True:
                    self.fireSound.play()
                    if self.multiplayerMode == True:
                        #sends fireSound data to cleints
                        self.player1.Send({"action": "playFireSound"})
                        self.player2.Send({"action": "playFireSound"})
                    player.fireBullet(self.player1WeaponLevel)
            #checks if player 2 fires a bullet
            else:
                self.player2Group.update(self.width, self.height)
                if self.gameMode2 == True:
                    self.movePlayer(player)
                if self.firing2 == True:
                    self.fireSound.play()
                    if self.multiplayerMode == True:
                        self.player1.Send({"action": "playFireSound"})
                        self.player2.Send({"action": "playFireSound"})
                    player.fireBullet(self.player2WeaponLevel)
        for bullet in player.bullets:
            #moves each bullet and removes when goes off screen
            bullet.move()
            if bullet.y < 0:
                player.bullets.remove(bullet)
            #checks to see if bullets hit enemies
            self.hitEnemy1(bullet, index)
            self.hitEnemy2(bullet, index)
            self.hitEnemy3(bullet, index)
            self.hitBoss(bullet, index)
        self.hitsPowerup(index)
        player.bullets.update(self.width,self.height)

    def hitPlayer(self, bullet, index=0):
        player = self.definePlayer(index)
        if player != None:
            playerBounds = (player.x,player.y,player.x,player.y)
            if isinstance(bullet, Bullet):
                bulletBounds = bullet.getBulletBounds()
            # boss can hit player in blitzMode
            elif isinstance(bullet, Enemy):
                bulletBounds = bullet.getEnemyBounds()
            if player.isHit == False:
                if self.boundsIntersect(bulletBounds,playerBounds):
                    self.playerHitSound.play()
                    if self.gameMode1 == True:
                        #if the bullet hits you you use a life
                        self.playerLives -= 1
                        if self.playerLives > 0: 
                            player = Player(self.width / 2, self.height / 2, 0)
                            self.playerGroup = pygame.sprite.Group(player)
                            player.isHit = True
                            #player loses power when hit
                            self.losePower()
                        else: self.isGameOver = True
                    elif self.gameMode2 == True or self.multiplayerMode == True:
                        if self.multiplayerMode == True:
                            self.player1.Send({"action": "playPlayerHitSound"})
                            self.player2.Send({"action": "playPlayerHitSound"})
                        if index == 0:
                            self.player1Lives -= 1
                            player.kill()
                            if self.player1Lives > 0:
                                player1 = Player(self.width/4, self.height/2, 0)
                                self.player1Group = pygame.sprite.Group(player1)
                                player1.isHit = True
                                #player loses power when hit
                                self.losePower(index)
                        else:
                            self.player2Lives -= 1
                            player.kill()
                            if self.player2Lives > 0:
                                player2 = Player(3*self.width/4, self.height/2,\
                                 1)
                                self.player2Group = pygame.sprite.Group(player2)
                                player2.isHit = True
                                #player loses power when hit
                                self.losePower(index)
                        if self.player1Lives == 0 and self.player2Lives == 0:
                            self.isGameOver = True

    def enemy1Event(self):
        self.enemy1Group.update(self.width,self.height)
        self.enemy1Timer += 1
        #spawns an enemy1 at a random x coordinate along the top
        if self.enemy1Timer == 50:
            self.enemy1Timer = 0
            enemyX = random.randint(30,450)
            enemyDir = random.randint(0,1)
            self.enemy1Group.add(Enemy1(enemyX,0,enemyDir))
        for enemy1 in self.enemy1Group:
            enemy1.bulletTimer += 1
            #enemy fires bullets at intervals
            if enemy1.bulletTimer == 20:
                enemy1.bulletTimer = 0
                enemy1.fireBullet()
            for bullet in enemy1.bullets:
                #checks to see if a bullet hits the player
                bullet.move()
                #removes bullets if it gets out of bounds
                if bullet.y > self.height or bullet.x < 0 or \
                bullet.x > self.width:
                    enemy1.bullets.remove(bullet)
                self.hitPlayer(bullet, 0)
                if self.gameMode2 == True or self.multiplayerMode == True:
                    self.hitPlayer(bullet, 1)
            enemy1.bullets.update(self.width,self.height)

    def enemy2Event(self):
        self.enemy2Group.update(self.width,self.height)
        self.enemy2Timer -= 1
        #spawns an enemy2 at a random x coordinate along the top
        if self.enemy2Timer == 0:
            self.enemy2Timer = 100
            enemyX = random.randint(30,450)
            self.enemy2Group.add(Enemy2(enemyX,0))
        for enemy2 in self.enemy2Group:
            enemy2.bulletTimer += 1
            #enemy fires bullets at intervals
            if enemy2.bulletTimer == 50:
                enemy2.bulletTimer = 0
                enemy2.fireBullet()
            for bullet in enemy2.bullets:
                #checks to see if a bullet hits the player
                bulletBounds = bullet.getBulletBounds()
                bullet.move()
                if bullet.y > self.height or bullet.x < 0 or \
                bullet.x > self.width:
                    enemy2.bullets.remove(bullet)
                self.hitPlayer(bullet, 0)
                if self.gameMode2 == True or self.multiplayerMode == True:
                    self.hitPlayer(bullet, 1)
            enemy2.bullets.update(self.width,self.height)

    def enemy3Event(self):
        self.enemy3Group.update(self.width,self.height)
        self.enemy3Timer -= 1
        #spans an enemy3 either from the left top or right top of screen
        if self.enemy3Timer == 0:
            self.enemy3Timer = 100
            movingRight = random.randint(0,1)
            #enemy will move right if it spawns on the left and vice versa
            if movingRight:
                self.enemy3Group.add(Enemy3(0,0,True))
            else:
                self.enemy3Group.add(Enemy3(self.width,0,False))
        for enemy3 in self.enemy3Group:
            enemy3.bulletTimer += 1
            #enemy fires bullets at intervals
            if enemy3.bulletTimer == 4:
                enemy3.bulletTimer = 0
                #enemy fires bullet at player
                if self.gameMode1 == True:
                    player = self.playerGroup.sprites()[0]
                    enemy3.fireBullet(player.x, player.y)
                #enemy randomly fires at both players
                elif self.gameMode2 == True or self.multiplayerMode == True:
                    if self.player1Lives > 0 and self.player2Lives>0:
                        randomPlayer = random.randint(0,1)
                    elif self.player1Lives > 0:
                        randomPlayer = 0
                    elif self.player2Lives > 0:
                        randomPlayer = 1
                    if randomPlayer == 0:
                        player = self.player1Group.sprites()[0]
                    else:
                        player = self.player2Group.sprites()[0]
                    enemy3.fireBullet(player.x, player.y)
            for bullet in enemy3.bullets:
                #checks to see if a bullet hits the player
                bulletBounds = bullet.getBulletBounds()
                bullet.move()
                if bullet.y > self.height or bullet.x < 0 or \
                bullet.x > self.width:
                    enemy3.bullets.remove(bullet)
                self.hitPlayer(bullet, 0)
                if self.gameMode2 == True or self.multiplayerMode == True:
                    self.hitPlayer(bullet, 1)
            enemy3.bullets.update(self.width,self.height)

    def bossEvent(self):
        self.bossGroup.update(self.width,self.height)
        self.bossTimer -= 1
        #spans an enemy3 either from the left top or right top of screen
        if self.bossTimer == 0:
            self.boss = Boss(self.width/2, 60)
            self.bossGroup.add(self.boss)
            #all other enemies are deleted when the boss is active
            for enemy1 in self.enemy1Group:
                enemy1.kill()
            for enemy2 in self.enemy2Group:
                enemy2.kill()
            for enemy3 in self.enemy3Group:
                enemy3.kill()
        for boss in self.bossGroup:
            #times the various bullets
            if boss.bullet1Timer > 0:
                boss.bullet1Timer -= 1
            if boss.bullet2Timer > 0:
                boss.bullet2Timer -= 1
            if boss.bullet3Timer > 0:
                boss.bullet3Timer -= 1
            if boss.bullet4Timer > 0:
                boss.bullet4Timer -= 1
            # boss fires different bullets at different stages of health
            if boss.health > 700: 
                if boss.bullet1Timer == 0:
                    boss.bullet1Timer = 1
                    if self.multiplayerMode == True:
                        boss.bullet1Timer = 3
                    boss.fireBullet1()
            #at 333 health, it goes into frenzy and attacks the player
            if boss.health < 400 and boss.blitzed == False:
                boss.blitzMode = 1
            if boss.health < 400 and boss.blitzMode == 0:
                boss.y = 60
                if boss.bullet4Timer == 0:
                    boss.bullet4Timer = 50
                    boss.fireBullet4()
            # 2nd stage, moves left and right, shooting two different bullets
            if boss.health <= 700 and boss.health >= 400: 
                if boss.bullet2Timer == 0:
                    boss.bullet2Timer = 10
                    boss.fireBullet2()
            if boss.health <= 700 and boss.health >= 400: 
                if boss.bullet3Timer == 0:
                    boss.bullet3Timer = 30
                    boss.fireBullet3()
            #boss collision is active
            self.hitPlayer(boss, 0)
            if self.gameMode2 == True or self.multiplayerMode == True:
                self.hitPlayer(boss, 1)
            for bullet in boss.bullets:
                #checks to see if a bullet hits the player
                bulletBounds = bullet.getBulletBounds()
                bullet.move()
                if bullet.y > self.height or bullet.x < 0 or \
                bullet.x > self.width:
                    bullet.kill()
                self.hitPlayer(bullet, 0)
                if self.gameMode2 == True or self.multiplayerMode == True:
                    self.hitPlayer(bullet, 1)
                # the fourth type of boss bullet splits into 4 after some time
                if type(bullet) == BossBullet4:
                    if bullet.timer <= 0:
                        if bullet.size-7 > 0:
                            for i in [1,3,5,7]:
                                #the bullets' speeds increase after split
                                newBullet = BossBullet4(bullet.x, bullet.y, \
                                    bullet.size-7, i*math.pi/4, \
                                    bullet.speed + 1)
                                boss.bullets.add(newBullet)
                        bullet.kill()
            boss.bullets.update(self.width,self.height)

    def losePower(self, index=0):
        if self.gameMode1 == True:
            #player goes down one power level when hit
            if self.playerPower == 3:
                self.enemyKillCount = 10
            else:
                self.enemyKillCount = 0
            if self.playerWeaponLevel > 1:
                self.playerWeaponLevel -= 1
        if self.gameMode2 == True or self.multiplayerMode == True:
            if index == 0:
                if self.player1Power == 3:
                    self.player1EnemyKillCount = 10
                else:
                    self.player1EnemyKillCount = 0
                if self.player1WeaponLevel > 1:
                    self.player1WeaponLevel -= 1
            else:
                if self.player2Power == 3:
                    self.player2EnemyKillCount = 10
                else:
                    self.player2EnemyKillCount = 0
                if self.player2WeaponLevel > 1:
                    self.player2WeaponLevel -= 1

    def abilityUsage(self):
        #slows down time if ability is used
        if self.abilityUsed == True:
            if self.abilityGauge > 0:
                #ability gauge/energy decreases
                self.abilityGauge -= 3
                self.abilityTimer = 30
                pygame.time.delay(100)
        #energy does not increase for a while after use
        if self.abilityTimer == 0:
            if self.abilityGauge < 100:
                self.abilityGauge += 1
        elif self.abilityTimer > 0:
            self.abilityTimer -= 1

    def bombUsage(self):
        #kills all enemies on screen when bomb is used
        if self.bombUsed == True:
            self.bombUseSound.play()
            if self.multiplayerMode == True:
                self.player1.Send({"action": "playBombUseSound"})
                self.player2.Send({"action": "playBombUseSound"})
            for enemy1 in self.enemy1Group:
                self.powerupAppear(enemy1)
                #makes explosion and plays sound for each enemy
                self.explosionGroup.add(Explosion(enemy1.x,\
                        enemy1.y, enemy1.width, enemy1.height))
                self.explodeSound.play()
                enemy1.kill()
                #adds the score of each enemy killed by the bomb
                self.totalScore += enemy1.score
            for enemy2 in self.enemy2Group:
                self.powerupAppear(enemy2)
                self.explosionGroup.add(Explosion(enemy2.x,\
                        enemy2.y, enemy2.width, enemy2.height))
                self.explodeSound.play()
                enemy2.kill()
                #adds the score of each enemy killed by the bomb
                self.totalScore += enemy2.score
            for enemy3 in self.enemy3Group:
                self.powerupAppear(enemy3)
                #centers the explosion on the enemy's body
                if enemy3.movingRight == True:
                    self.explosionGroup.add(Explosion(enemy3.x+40,\
                        enemy3.y, 48, enemy3.height))
                else:
                    self.explosionGroup.add(Explosion(enemy3.x-40,\
                        enemy3.y, 48, enemy3.height))
                self.explodeSound.play()
                enemy3.kill()
                #adds the score of each enemy killed by the bomb
                self.totalScore += enemy3.score
            for boss in self.bossGroup:
                boss.health -= 75
                boss.bullets = pygame.sprite.Group()
                #enemy dies if its health reaches 0
                if boss.health <= 0:
                    self.explosionGroup.add(Explosion(boss.x,\
                        boss.y, boss.width, boss.height))
                    boss.kill()
                    self.explodeSound.play()
                    if self.multiplayerMode == True:
                        self.player1.Send({"action": "playExplodeSound"})
                        self.player2.Send({"action": "playExplodeSound"})
                    #adds the score of the hit enemy
                    self.totalScore += boss.score
                    self.gameWon = True
            self.bombUsed = False
            self.bombAnimationTimer = 0

    def powerupEvent(self):
        #the powerups only remain for a temporary amount of time
        for bombup in self.bombupGroup:
            bombup.timer += 1
            if bombup.timer > 140:
                bombup.kill()
        #updates the sprite group
        self.bombupGroup.update(self.width, self.height)
        for lifeup in self.lifeupGroup:
            lifeup.timer += 1
            if lifeup.timer > 140:
                lifeup.kill()
        self.lifeupGroup.update(self.width, self.height)
        for weaponup in self.weaponupGroup:
            weaponup.timer += 1
            if weaponup.timer > 140:
                weaponup.kill()
        self.weaponupGroup.update(self.width, self.height)

    def explosionEvent(self):
        #explosion event ends after animated sprite finishes
        for explosion in self.explosionGroup:
            if explosion.index >= 18:
                explosion.kill()
        self.explosionGroup.update(self.width, self.height)

    def cloudEvent(self):
        #clouds continuously move down and wrap around to simulate flying
        for cloud in self.cloudGroup:
            cloud.move(self.height)
        self.cloudGroup.update(self.width, self.height)

    def powerupAppear(self,enemy):
        #power up randomly appears when enemies are killed
        powerupChance = random.randint(0,3)
        if powerupChance == 0:
            self.bombupGroup.add(Bombup(enemy.x, enemy.y))
        elif powerupChance == 1:
            self.lifeupGroup.add(Lifeup(enemy.x, enemy.y))
        elif powerupChance == 2:
            self.weaponupGroup.add(Weaponup(enemy.x, enemy.y))

    def updatePlayerHelper(self):
        #update player 1 & 2 separately so if one dies the other can still play
        if self.player1Lives > 0:
            player1 = self.player1Group.sprites()[0]
            #updates information to client side
            data = {"action": "updateplayer1", "player1X": player1.x, \
            "player1Y": player1.y, "player1Index":player1.index,\
            "player1Timer": player1.timer, "player1Countdown": \
            player1.countdown, "player1Hit": player1.isHit, "gameid": \
            self.gameid, "type": 1}
            self.player1.Send(data)
            self.player2.Send(data)
        #data is separate from player details so player disappears after death
        data = {"action": "updateplayer1", "player1Lives": self.player1Lives, \
            "player1Power": self.player1Power, "player1Bombs": \
            self.player1Bombs, "player1Weapon": self.player1WeaponLevel, \
            "gameid": self.gameid, "type": 2}
        self.player1.Send(data)
        self.player2.Send(data)

        if self.player2Lives > 0:
            player2 = self.player2Group.sprites()[0]
            #updates information to client side
            data = {"action": "updateplayer2", "player2X": player2.x, \
            "player2Y": player2.y, "player2Index":player2.index, \
            "player2Timer": player2.timer, "player2Countdown": \
            player2.countdown, "player2Hit": player2.isHit, "gameid": \
            self.gameid, "type": 1}
            self.player1.Send(data)
            self.player2.Send(data)
        data = {"action": "updateplayer2", "player2Lives": self.player2Lives, \
            "player2Power": self.player2Power, "player2Bombs": \
            self.player2Bombs, "player2Weapon": self.player2WeaponLevel, \
            "gameid": self.gameid, "type": 2}
        self.player1.Send(data)
        self.player2.Send(data)

    def updatePlayerBulletsHelper(self):
        #updates the players' bullets
        if self.player1Lives > 0:
            player1 = self.player1Group.sprites()[0]
            for bullet in player1.bullets:
                data = {"action": "updatePlayerBullets", "x":bullet.x,\
                "y": bullet.y, "size": bullet.size, "player": 1}
                self.player1.Send(data)
                self.player2.Send(data)
        #separate for the two players so only updates if player is alive
        if self.player2Lives > 0:
            player2 = self.player2Group.sprites()[0]
            for bullet in player2.bullets:
                data = {"action": "updatePlayerBullets", "x":bullet.x,\
                "y": bullet.y, "size": bullet.size, "player": 2}
                self.player1.Send(data)
                self.player2.Send(data)

    def updateEnemy1Helper(self):
        #updates enemy 1 to client
        for enemy1 in self.enemy1Group:
            data = {"action": "updateEnemies", "x": enemy1.x, \
            "y": enemy1.y, "health": enemy1.health, "bulletTimer":\
            enemy1.bulletTimer, "direction": enemy1.direction, \
            "enemyType": 1}
            self.player1.Send(data)
            self.player2.Send(data)
            #updates three different types of enemy1 bullets
            for bullet in enemy1.bullets:
                if type(bullet) == Enemy1BulletMid:
                    bulletType = 1
                if type(bullet) == Enemy1BulletLeft:
                    bulletType = 2
                else:
                    bulletType = 3
                data = {"action": "updateEnemy1Bullets", "x": \
                bullet.x, "y": bullet.y, "size": bullet.size, \
                "bulletType": bulletType}
                self.player1.Send(data)
                self.player2.Send(data)

    def updateEnemy2Helper(self):
        #updates enemy2
        for enemy2 in self.enemy2Group:
            data = {"action": "updateEnemies", "x": enemy2.x, \
            "y": enemy2.y, "health": enemy2.health, "bulletTimer":\
            enemy2.bulletTimer, "index": enemy2.index, "enemyType": 2}
            self.player1.Send(data)
            self.player2.Send(data)
            #updates enemy2 bullets
            for bullet in enemy2.bullets:
                data = {"action": "updateEnemy2Bullets", "x": \
                bullet.x, "y": bullet.y, "size": bullet.size, "angle": \
                bullet.angle}
                self.player1.Send(data)
                self.player2.Send(data)

    def updateEnemy3Helper(self):
        #updates enemy3 sprites
        for enemy3 in self.enemy3Group:
            data = {"action": "updateEnemies", "x": enemy3.x, \
            "y": enemy3.y, "health": enemy3.health, "bulletTimer":\
            enemy3.bulletTimer, "movingRight": enemy3.movingRight,\
            "index": enemy3.index, "enemyType": 3}
            self.player1.Send(data)
            self.player2.Send(data)
            #updates enemy3 bullets
            for bullet in enemy3.bullets:
                data = {"action": "updateEnemy3Bullets", "x": \
                bullet.x, "y": bullet.y, "size": bullet.size, "xDistance": \
                bullet.xDistance, "yDistance": bullet.yDistance, \
                "timesMove": bullet.timesMove, "xMoveInterval": \
                bullet.xMoveInterval}
                self.player1.Send(data)
                self.player2.Send(data)

    def updateBossHelper(self):
        #updates the boss information to client
        for boss in self.bossGroup:
            data = {"action": "updateEnemies", "x": boss.x, \
            "y": boss.y, "health": boss.health, "bullet1Timer": \
            boss.bullet1Timer, "bullet2Timer": boss.bullet2Timer,\
            "bullet3Timer": boss.bullet3Timer, "movingRight": \
            boss.movingRight, "index": boss.index, "delta": \
            boss.delta, "blitzMode": boss.blitzMode, "blitzed": boss.blitzed,\
            "direction": boss.direction, "enemyType": 4}
            self.player1.Send(data)
            self.player2.Send(data)
            #updates the four types of boss bullets
            for bullet in boss.bullets:
                if type(bullet) == BossBullet1:
                    bulletType = 1
                elif type(bullet) == BossBullet2:
                    bulletType = 2
                elif type(bullet) == BossBullet3:
                    bulletType = 3
                elif type(bullet) == BossBullet4:
                    bulletType = 4
                if bulletType == 1:
                    data = {"action": "updateBossBullets", "x": \
                    bullet.x, "y": bullet.y, "size": bullet.size, \
                    "bulletType": bulletType, "angle": bullet.angle, "delta": \
                    bullet.delta}
                    self.player1.Send(data)
                    self.player2.Send(data)
                if bulletType == 2:
                    data = {"action": "updateBossBullets", "x": \
                    bullet.x, "y": bullet.y, "size": bullet.size, \
                    "bulletType": bulletType, "dx": bullet.dx}
                    self.player1.Send(data)
                    self.player2.Send(data)
                if bulletType == 3:
                    data = {"action": "updateBossBullets", "x": \
                    bullet.x, "y": bullet.y, "size": bullet.size, \
                    "bulletType": bulletType, "angle": bullet.angle}
                    self.player1.Send(data)
                    self.player2.Send(data)
                if bulletType == 4:
                    data = {"action": "updateBossBullets", "x": \
                    bullet.x, "y": bullet.y, "size": bullet.size, \
                    "bulletType": bulletType, "angle": bullet.angle, \
                    "speed": bullet.speed, "timer": bullet.timer}

    def updatePowerupsHelper(self):
        #resets the powerup groups so they don't stack
        self.player1.Send({"action": "resetPowerups"})
        self.player2.Send({"action": "resetPowerups"})
        #updates bombups, lifeups, and weaponups
        for bombup in self.bombupGroup:
            data = {"action": "updatePowerups", "x": bombup.x, "y": bombup.y, \
            "timer": bombup.timer, "type": 1}
            self.player1.Send(data)
            self.player2.Send(data)
        for lifeup in self.lifeupGroup:
            data = {"action": "updatePowerups", "x": lifeup.x, "y": lifeup.y, \
            "timer": lifeup.timer, "type": 2}
            self.player1.Send(data)
            self.player2.Send(data)
        for weaponup in self.weaponupGroup:
            data = {"action": "updatePowerups", "x": weaponup.x, "y": \
            weaponup.y, "timer": weaponup.timer, "type": 3}
            self.player1.Send(data)
            self.player2.Send(data)

    def updateExplosionsHelper(self):
        #resets explosions before update so they don't stack
        self.player1.Send({"action": "resetExplosions"})
        self.player2.Send({"action": "resetExplosions"})
        #updates explosion information
        for explosion in self.explosionGroup:
            data = {"action": "updateExplosions", "x": explosion.x, \
            "y": explosion.y, "width": explosion.width, "height": \
            explosion.height, "index": explosion.index}
            self.player1.Send(data)
            self.player2.Send(data)

    def updateGameInfo(self):
        #updates other various game info to clients
        data = {"action": "updateGameInfo", "score": self.totalScore, \
        "gameover": self.isGameOver, "gamewon": self.gameWon, \
        "bombanimation": self.bombAnimationTimer}
        self.player1.Send(data)
        self.player2.Send(data)

    def timerFired(self, dt):
        # game plays if it's not paused
        if not self.isPaused:
            if self.gameMode1 == True:
                #if not game over and game not won
                if self.isGameOver == False and self.gameWon == False:
                    self.playerMovement()
                    self.abilityUsage()
                    self.bossEvent()
                    if self.bossTimer > 0:
                        self.enemy1Event()
                        self.enemy2Event()
                        self.enemy3Event()
                    self.bombUsage()
                    self.powerupEvent()
                    self.explosionEvent()
                    self.cloudEvent()
                    #player power increases from enemies killed to a max of 3
                    self.playerPower = 1 + self.enemyKillCount//10
                    if self.playerPower >= 3:
                        self.playerPower = 3
                elif self.isGameOver == True or self.gameWon == True:
                    # you can enter a name into the textbox at end of game
                    if self.nameEnterDone == False:
                        events = pygame.event.get()
                        keyEntered = self.textbox.update(events)
                        if keyEntered != None:
                            self.nameEnterDone = True
            elif self.gameMode2 == True or (self.multiplayerMode == True and \
                self.gameStarted == True):
                if self.isGameOver == False and self.gameWon == False:
                    if self.player1Lives > 0:
                        self.playerMovement(0)
                    if self.player2Lives > 0:
                        self.playerMovement(1)
                    self.bossEvent()
                    if self.bossTimer > 0:
                        self.enemy1Event()
                        self.enemy2Event()
                        self.enemy3Event()
                    self.bombUsage()
                    self.powerupEvent()
                    self.explosionEvent()
                    self.cloudEvent()
                    #player power increases from enemies killed up to a max of 3
                    self.player1Power = 1 + self.player1EnemyKillCount//10
                    self.player2Power = 1 + self.player2EnemyKillCount//10
                    if self.player1Power >= 3:
                        self.player1Power = 3
                    if self.player2Power >= 3:
                        self.player2Power = 3
                    if self.multiplayerMode == True:
                        #updates data to client
                        self.updatePlayerHelper()
                        self.updatePlayerBulletsHelper()
                        #resets enemy sprites and bullet sprites
                        self.player1.Send({"action": "resetEnemies"})
                        self.player2.Send({"action": "resetEnemies"})
                        self.player1.Send({"action": "resetBullets"})
                        self.player2.Send({"action": "resetBullets"})
                        self.updateEnemy1Helper()
                        self.updateEnemy2Helper()
                        self.updateEnemy3Helper()
                        self.updateBossHelper()
                        self.updatePowerupsHelper()
                        self.updateExplosionsHelper()
                        self.updateGameInfo()
                        if self.bombAnimationTimer >= 0:
                            self.bombAnimationTimer += 1
                            if self.bombAnimationTimer == 30:
                                self.bombAnimationTimer = -1

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

    def drawNormalGameScreen(self, screen):
        #draws background clouds
        self.cloudGroup.draw(screen)
        #draws the player, enemies and bullets
        player = self.playerGroup.sprites()[0]
        if player.countdown % 2 == 0:
            self.playerGroup.draw(screen)
        player.bullets.draw(screen)
        self.drawEnemies(screen)
        self.drawPowerups(screen)
        #draws explosions
        self.explosionGroup.draw(screen)
        #draws the score on bottom right
        scoreFont = pygame.font.Font("Audiowide.ttf", 14, bold=True)
        scoreMessage = scoreFont.render("Score: %d" % self.totalScore,\
         1, (255,255,255))
        screen.blit(scoreMessage, (self.width - 80, self.height - 40))
        #draws the player power level on bottom right
        powerFont = pygame.font.Font("Audiowide.ttf", 14, bold=True)
        if self.playerPower < 3:
            powerMessage = powerFont.render("Power: %d" % self.playerPower,\
             1, (255,255,255))
        else:
            powerMessage = powerFont.render("Power: MAX",\
             1, (255,255,255))
        screen.blit(powerMessage, (self.width - 80, self.height - 60))
        #draws the lives on bottom left
        livesFont = pygame.font.Font("Audiowide.ttf", 14, bold=True)
        livesMessage = livesFont.render("Lives: %d" % self.playerLives,\
         1, (255,255,255))
        screen.blit(livesMessage, (30, self.height - 60))
        #draws the bombs on bottom left
        bombsFont = pygame.font.Font("Audiowide.ttf", 14, bold=True)
        bombsMessage = bombsFont.render("Bombs: %d" % self.playerBombs,\
         1, (255,255,255))
        screen.blit(bombsMessage, (30, self.height - 40))
        
        #draws the ability gauge on left of screen
        pygame.draw.rect(screen,(0,0,0),((50,560),\
            (10,-100)))
        pygame.draw.rect(screen,(255,255,0),((50,560),\
            (10,-self.abilityGauge)))

        #draws special mouse pointer for game
        #idea from Andy Shen
        self.mouseImageIndex += 1
        if self.mouseImageIndex >= len(self.mouseImages):
            self.mouseImageIndex = 0
        self.mouseImage = pygame.transform.scale(self.mouseImages\
            [self.mouseImageIndex].convert_alpha(),(24,24))
        pygame.mouse.set_visible(False)
        (x,y) = pygame.mouse.get_pos()
        screen.blit(self.mouseImage, (x-12,y-12))

        if self.isPaused == True:
            pauseFont = pygame.font.Font("Audiowide.ttf", 20)
            pause = pauseFont.render("Paused", 1, (255,255,255))
            pausePos = pause.get_rect()
            pausePos.centerx = screen.get_size()[0]/2
            pausePos.centery = screen.get_size()[1]/2
            screen.blit(pause, pausePos)


    def drawPlayer1Details(self, screen):
        #tells you that its player 1
        player1Font = pygame.font.Font("Audiowide.ttf", 18, bold=True)
        player1Font.set_underline(1)
        player1Message = player1Font.render("Player 1",\
         1, (255,255,255))
        screen.blit(player1Message, (30, self.height - 110))
        #draws player1 power level on bottom left
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
        #draws the player power level on bottom right
        powerFont = pygame.font.Font("Audiowide.ttf", 14, bold=True)
        if self.player2Power < 3:
            powerMessage = powerFont.render("Power: %d" % self.player2Power,\
             1, (255,255,255))
        else:
            powerMessage = powerFont.render("Power: MAX",\
             1, (255,255,255))
        screen.blit(powerMessage, (self.width - 80, self.height - 80))
        #draws the lives on bottom right
        livesFont = pygame.font.Font("Audiowide.ttf", 14, bold=True)
        livesMessage = livesFont.render("Lives: %d" % self.player2Lives,\
         1, (255,255,255))
        screen.blit(livesMessage, (self.width - 80, self.height - 60))
        #draws the bombs on bottom right
        bombsFont = pygame.font.Font("Audiowide.ttf", 14, bold=True)
        bombsMessage = bombsFont.render("Bombs: %d" % self.player2Bombs,\
         1, (255,255,255))
        screen.blit(bombsMessage, (self.width - 80, self.height - 40))

    def drawTwoPlayerScreen(self, screen):
        #draws background clouds
        self.cloudGroup.draw(screen)
        #draws both players and their bullets
        if self.player1Lives > 0:
            player1 = self.player1Group.sprites()[0]
            if player1.countdown % 2 == 0:
                self.player1Group.draw(screen)
            player1.bullets.draw(screen)
        if self.player2Lives > 0:
            player2 = self.player2Group.sprites()[0]
            if player2.countdown % 2 == 0:
                self.player2Group.draw(screen)
            player2.bullets.draw(screen)
        #draws the enemies and powerups
        self.drawEnemies(screen)
        self.drawPowerups(screen)
        #draws explosions
        self.explosionGroup.draw(screen)
        #draws the score on top right
        scoreFont = pygame.font.Font("Audiowide.ttf", 14, bold=True)
        scoreMessage = scoreFont.render("Score: %d" % self.totalScore,\
         1, (0,0,0))
        scorePos = scoreMessage.get_rect()
        scorePos.top = 30
        scorePos.right = self.width-10
        screen.blit(scoreMessage, scorePos)
        self.drawPlayer1Details(screen)
        self.drawPlayer2Details(screen)
        
        #draws special mouse pointer for game
        #idea from Andy Shen
        self.mouseImageIndex += 1
        if self.mouseImageIndex >= len(self.mouseImages):
            self.mouseImageIndex = 0
        self.mouseImage = pygame.transform.scale(self.mouseImages\
            [self.mouseImageIndex].convert_alpha(),(24,24))
        pygame.mouse.set_visible(False)
        (x,y) = pygame.mouse.get_pos()
        screen.blit(self.mouseImage, (x-12,y-12))

        #blits paused text
        if self.isPaused == True:
            pauseFont = pygame.font.Font("Audiowide.ttf", 20)
            pause = pauseFont.render("Paused", 1, (255,255,255))
            pausePos = pause.get_rect()
            pausePos.centerx = screen.get_size()[0]/2
            pausePos.centery = screen.get_size()[1]/2
            screen.blit(pause, pausePos)

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
        if self.gameMode1 == True:
            restartFont = pygame.font.Font("Crushed.ttf", 13)
            submitName = restartFont.render("Press Enter Once to Submit Name",\
                1, (255,255,255))
            submitNamePos = submitName.get_rect()
            submitNamePos.centerx = screen.get_size()[0]/2
            submitNamePos.centery = screen.get_size()[1]/2 + 200
            screen.blit(submitName, submitNamePos)
            restart = restartFont.render("Press Enter to Go Back to Main Menu"\
                , 1, (255,255,255))
            restartPos = restart.get_rect()
            restartPos.centerx = screen.get_size()[0]/2
            restartPos.centery = screen.get_size()[1]/2 + 225
            screen.blit(restart, restartPos)

            #Enter player name text box
            self.textbox.set_pos(screen.get_size()[0]/2, \
                screen.get_size()[1]/2 + 40)
            self.textbox.draw(screen)
        elif self.gameMode2 == True:
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
        gameWonPos.centery = screen.get_size()[1]/2 - 60
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
        if self.gameMode1 == True:
            restartFont = pygame.font.Font("Crushed.ttf", 13)
            submitName = restartFont.render("Press Enter Once to Submit Name",\
                1, (255,255,255))
            submitNamePos = submitName.get_rect()
            submitNamePos.centerx = screen.get_size()[0]/2
            submitNamePos.centery = screen.get_size()[1]/2 + 200
            screen.blit(submitName, submitNamePos)
            restart = restartFont.render("Press Enter to Go Back to Main Menu"\
                , 1, (255,255,255))
            restartPos = restart.get_rect()
            restartPos.centerx = screen.get_size()[0]/2
            restartPos.centery = screen.get_size()[1]/2 + 225
            screen.blit(restart, restartPos)

            #Enter player name text box
            self.textbox.set_pos(screen.get_size()[0]/2, \
                screen.get_size()[1]/2 + 40)
            self.textbox.draw(screen)
        elif self.gameMode2 == True:
            restartFont = pygame.font.Font("Crushed.ttf", 13)
            restart = restartFont.render("Press Enter to Go Back to Main Menu"\
                , 1, (255,255,255))
            restartPos = restart.get_rect()
            restartPos.centerx = screen.get_size()[0]/2
            restartPos.centery = screen.get_size()[1]/2 + 225
            screen.blit(restart, restartPos)

    '''Created by Alistair Buxton found online
    http://archives.seul.org/pygame/users/Mar-2008/msg00538.html '''
    def DrawRoundRect(self, surface, color, rect, width, xr, yr):
        clip = surface.get_clip()
        
        # left and right
        surface.set_clip(clip.clip(rect.inflate(0, -yr*2)))
        pygame.draw.rect(surface, color, rect.inflate(1-width,0), width)

        # top and bottom
        surface.set_clip(clip.clip(rect.inflate(-xr*2, 0)))
        pygame.draw.rect(surface, color, rect.inflate(0,1-width), width)

        # top left corner
        surface.set_clip(clip.clip(rect.left, rect.top, xr, yr))
        pygame.draw.ellipse(surface, color, pygame.Rect(rect.left, rect.top, \
            2*xr, 2*yr), width)

        # top right corner
        surface.set_clip(clip.clip(rect.right-xr, rect.top, xr, yr))
        pygame.draw.ellipse(surface, color, pygame.Rect(rect.right-2*xr, \
            rect.top, 2*xr, 2*yr), width)

        # bottom left
        surface.set_clip(clip.clip(rect.left, rect.bottom-yr, xr, yr))
        pygame.draw.ellipse(surface, color, pygame.Rect(rect.left, \
            rect.bottom-2*yr, 2*xr, 2*yr), width)

        # bottom right
        surface.set_clip(clip.clip(rect.right-xr, rect.bottom-yr, xr, yr))
        pygame.draw.ellipse(surface, color, pygame.Rect(rect.right-2*xr, \
            rect.bottom-2*yr, 2*xr, 2*yr), width)

        surface.set_clip(clip)

    def drawMainMenu(self, screen):
        #Game Title
        #Crushed font was created by Hypefonts on fontspace.com
        titleFont = pygame.font.Font('Crushed.ttf', 40)
        title1 = titleFont.render("Bullet"\
            , 1, (255,255,255))
        title1Pos = title1.get_rect()
        title1Pos.centerx = 240
        title1Pos.centery = 77
        screen.blit(title1, title1Pos)
        title2 = titleFont.render("Armageddon"\
            , 1, (255,255,255))
        title2Pos = title2.get_rect()
        title2Pos.centerx = 240
        title2Pos.centery = 140
        screen.blit(title2, title2Pos)
        #menu button outline
        self.DrawRoundRect(screen,(255,255,255),pygame.Rect(137,197,206,66), \
            0, 32, 64)
        self.DrawRoundRect(screen,(255,255,255),pygame.Rect(137,277,206,66), \
            0, 32, 64)
        self.DrawRoundRect(screen,(255,255,255),pygame.Rect(137,357,206,66), \
            0, 32, 64)
        self.DrawRoundRect(screen,(255,255,255),pygame.Rect(137,437,206,66), \
            0, 32, 64)
        self.DrawRoundRect(screen,(255,255,255),pygame.Rect(137,517,206,66), \
            0, 32, 64)
        #menu buttons
        self.DrawRoundRect(screen,(0,0,0),pygame.Rect(140,200,200,60), \
            0, 64, 64)
        self.DrawRoundRect(screen,(0,0,0),pygame.Rect(140,280,200,60), \
            0, 64, 64)
        self.DrawRoundRect(screen,(0,0,0),pygame.Rect(140,360,200,60), \
            0, 64, 64)
        self.DrawRoundRect(screen,(0,0,0),pygame.Rect(140,440,200,60), \
            0, 64, 64)
        self.DrawRoundRect(screen,(0,0,0),pygame.Rect(140,520,200,60), \
            0, 64, 64)
        #text on menu buttons
        menuFont = pygame.font.Font("Crushed.ttf", 14)
        singlePlayer = menuFont.render("1 Player"\
            , 1, (255,255,255))
        singlePlayerPos = singlePlayer.get_rect()
        singlePlayerPos.centerx = 240
        singlePlayerPos.centery = 230
        screen.blit(singlePlayer, singlePlayerPos)
        twoPlayer = menuFont.render("2 Player"\
            , 1, (255,255,255))
        twoPlayerPos = twoPlayer.get_rect()
        twoPlayerPos.centerx = 240
        twoPlayerPos.centery = 310
        screen.blit(twoPlayer, twoPlayerPos)
        multiPlayer = menuFont.render("Server"\
            , 1, (255,255,255))
        multiPlayerPos = twoPlayer.get_rect()
        multiPlayerPos.centerx = 250
        multiPlayerPos.centery = 390
        screen.blit(multiPlayer, multiPlayerPos)
        instructions = menuFont.render("Instructions"\
            , 1, (255,255,255))
        instructionsPos = instructions.get_rect()
        instructionsPos.centerx = 240
        instructionsPos.centery = 470
        screen.blit(instructions, instructionsPos)
        highScores = menuFont.render("High Scores"\
            , 1, (255,255,255))
        highScoresPos = highScores.get_rect()
        highScoresPos.centerx = 240
        highScoresPos.centery = 550
        screen.blit(highScores, highScoresPos)

    def drawHighScores(self, screen):
        highScoreNames = []
        highScorePoints = []
        scoresAndNames = []
        #reads high scores from a file
        with open("file.txt", "r") as highscores_file:
            for line in highscores_file:
                scoresAndNames.append(line)
            #sorts by score
            scoresAndNames = sorted(scoresAndNames)
            scoresAndNames = reversed(scoresAndNames)
            for i in scoresAndNames:
                splitList = i.split("/")
                score = splitList[0]
                name = splitList[1][:-1]
                #adds the names and points to separate lists in order
                highScorePoints.append(score)
                highScoreNames.append(name)
        scoreFont = pygame.font.Font("Audiowide.ttf", 20)
        #draws the top 10 high scores
        highScoreTitleFont = pygame.font.Font("Audiowide.ttf", 26)
        highScoreTitleFont.set_underline(1)
        highScoreName = highScoreTitleFont.render("Player Name"\
                    , 1, (255,255,255))
        screen.blit(highScoreName, (30, 150))
        highScore = highScoreTitleFont.render("Score"\
            , 1, (255,255,255))
        highScorePos = highScore.get_rect()
        highScorePos.top = 150
        highScorePos.right = self.width-25
        screen.blit(highScore, highScorePos)
        for i in range(9):
            if i < (len(highScorePoints)):
                scoreName = scoreFont.render(highScoreNames[i]\
                    , 1, (255,255,255))
                screen.blit(scoreName, (30, 200 + 42*i))
                score = scoreFont.render(str(highScorePoints[i])\
                    , 1, (255,255,255))
                scorePos = score.get_rect()
                scorePos.top = 200 + 42*i
                scorePos.right = self.width-25
                screen.blit(score, scorePos)
        #return to main menu
        returnMainMenuFont = pygame.font.Font("Audiowide.ttf", 18, bold=True)
        returnMainMenu = returnMainMenuFont.render(\
            "Press Backspace to go back to Main Menu.", \
            1, (255,255,255))
        screen.blit(returnMainMenu, (30, 600))

    def drawInstructions(self, screen):
        #blits lines of instructions onto the screen
        instructionsTitleFont = pygame.font.Font("Audiowide.ttf", 18, bold=True)
        instructionsTitleFont.set_underline(1)
        instructionsTitle1 = instructionsTitleFont.render("Single Player Mode"\
            , 1, (255,255,255))
        screen.blit(instructionsTitle1, (20, 30))
        instructionsFont = pygame.font.Font("Audiowide.ttf", 11)
        instructions1 = instructionsFont.render(\
            "Use either the mouse or the arrow keys to move the player.", \
            1, (255,255,255))
        screen.blit(instructions1, (20, 60))
        instructions2 = instructionsFont.render(\
            "Press the left mouse button or the 'z' key to shoot.", \
            1, (255,255,255))
        screen.blit(instructions2, (20, 90))
        instructions3 = instructionsFont.render(\
        "Press the right mouse button or the 'x' key to use a bomb and kill",\
        1, (255,255,255))
        screen.blit(instructions3, (20, 120))
        instructions32 = instructionsFont.render("all enemies on screen", \
            1, (255,255,255))
        screen.blit(instructions32, (20,135))
        instructions4 = instructionsFont.render(\
        "Press space or shift to use your ability to slow time. This drains", \
        1, (255,255,255))
        screen.blit(instructions4, (20, 165))
        instructions42 = instructionsFont.render(\
            "your energy bar, which will slowly refill.", 1, (255,255,255))
        screen.blit(instructions42, (20,180))
        instructions6 = instructionsFont.render(\
        "You start out with three lives and three bombs, but can get more", \
        1, (255,255,255))
        screen.blit(instructions6, (20, 210))
        instructions62 = instructionsFont.render(\
            "from powerups, which drop after enemies die.", 1, (255,255,255))
        screen.blit(instructions62, (20, 225))
        instructions7 = instructionsFont.render(\
        "The 'P' powerup will increase your weapon level so you can",\
         1, (255,255,255))
        screen.blit(instructions7, (20, 255))
        instructions72 = instructionsFont.render(\
            "shoot more bullets at enemies.", 1, (255,255,255))
        screen.blit(instructions72, (20, 270))
        instructions8 = instructionsFont.render(\
        "Your weapon also gains power when you kill a certain amount of",\
         1, (255,255,255))
        screen.blit(instructions8, (20, 300))
        instructions82 = instructionsFont.render(\
            "enemies, and will do more damage.", 1, (255,255,255))
        screen.blit(instructions82, (20, 315))
        instructionsTitle2 = instructionsTitleFont.render("Two Player Mode"\
            , 1, (255,255,255))
        screen.blit(instructionsTitle2, (20, 365))
        instructions10 = instructionsFont.render(\
            "Two player mode is similar to single player mode.", \
            1, (255,255,255))
        screen.blit(instructions10, (20, 395))
        instructions11 = instructionsFont.render(\
        "However, the first player uses the mouse to move while the second",\
         1, (255,255,255))
        screen.blit(instructions11, (20, 425))
        instructions112 = instructionsFont.render(\
            "uses the arrow keys.", 1, (255,255,255))
        screen.blit(instructions112, (20, 440))
        instructions12 = instructionsFont.render(\
            "The first player shoots with the left mouse button and uses", \
            1, (255,255,255))
        screen.blit(instructions12, (20, 470))
        instructions122 = instructionsFont.render(\
            "bombs with the right.", 1, (255,255,255))
        screen.blit(instructions122, (20, 485))
        instructions13 = instructionsFont.render(\
            "The second player uses 'z' to shoot and 'x' to use bombs.", \
            1, (255,255,255))
        screen.blit(instructions13, (20, 515))
        instructions15 = instructionsFont.render(\
            "Each player has separate lives, bombs, powers, and weapon",\
             1, (255,255,255))
        screen.blit(instructions15, (20, 545))
        instructions152 = instructionsFont.render(\
            "levels, but share a total score.", 1, (255,255,255))
        screen.blit(instructions152, (20, 560))
        instructionsTitleFont.set_underline(0)
        instructionsTitle3 = instructionsTitleFont.render(\
            "Press Backspace to go back to Main Menu.", \
            1, (255,255,255))
        screen.blit(instructionsTitle3, (20, 600))

    def redrawAll(self, screen):
        if self.gameMode1 == True:
            if self.isGameOver == False and self.gameWon == False:
                self.drawNormalGameScreen(screen)
                #draws bomb animation
                if self.bombAnimationTimer >= 0:
                    if self.bombAnimationTimer % 5 == 0:
                        screen.fill((255,255,255))
                    self.bombAnimationTimer += 1
                    if self.bombAnimationTimer == 30:
                        self.bombAnimationTimer = -1
            elif self.isGameOver == True:
                self.drawGameOverScreen(screen)
            else:
                self.drawGameWonScreen(screen)
        elif self.gameMode2 == True:
            if self.isGameOver == False and self.gameWon == False:
                self.drawTwoPlayerScreen(screen)
                #draws bomb animation
                if self.bombAnimationTimer >= 0:
                    if self.bombAnimationTimer % 5 == 0:
                        screen.fill((255,255,255))
                    self.bombAnimationTimer += 1
                    if self.bombAnimationTimer == 30:
                        self.bombAnimationTimer = -1
            elif self.isGameOver == True:
                self.drawGameOverScreen(screen)
            else:
                self.drawGameWonScreen(screen)
        #draws the menu pages
        elif self.menuMode == True:
            #makes mouse visible
            pygame.mouse.set_visible(True)
            self.drawMainMenu(screen)
        elif self.instructionsMode == True:
            pygame.mouse.set_visible(True)
            self.drawInstructions(screen)
        elif self.highScoresMode == True:
            pygame.mouse.set_visible(True)
            self.drawHighScores(screen)
        self.screen = screen

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, player1=None, currentIndex=None, width=480, height=640, fps=15, title="Term Project"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.player1 = player1
        self.player2 = None
        self.gameid = currentIndex
        '''Menu background from \
        http://topwalls.net/wallpapers/2012/11/Wallpaper-Rays-Color-\
        Black-Background-640x480.jpg'''
        self.bg = pygame.image.load("images/mainmenu.jpg")
        pygame.init()

    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        self.screen = screen
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
            if self.gameMode1 == True or self.gameMode2 == True:
                '''Background image is from 
                http://1.bp.blogspot.com/-iMMViPyVOnk/Ukr \
                iYf7srMI/AAAAAAAACJs/70U17vjatQI/s640/P1010098.jpg'''
                self.bg = pygame.image.load("images/bg.jpg")
            elif self.instructionsMode == True:
                '''Background image is from
                http://wallpaperswiki.org/wallpapers/2012/11/Wallpaper-Line-\
                Node-Lights-Background-Abstract-640x480.jpg'''
                self.bg = pygame.image.load("images/instructions.jpg")
            elif self.highScoresMode == True:
                '''Background image is from
                http://img.wallsus.com/download/20140228/abstraction,\
                -abstraction,-background,-rays,-band,-band,-line,-line,-light,\
                -lights-480x640.jpg'''
                self.bg = pygame.image.load("images/highscores.jpg")
            elif self.menuMode == True:
                self.bg = pygame.image.load("images/mainmenu.jpg")
            screen.blit(self.bg, (0, 0))
            if self.isGameOver == True:
                screen.fill((0,0,0))
            self.redrawAll(screen)
            pygame.display.flip()

            # pygame.quit()z

    def multiPlayerShoot(self, data, num):
        #player 1
        if num == 0:
            #server functions for shooting from client input
            if self.firing1 == True:
                self.firing1 = False
            else:
                self.firing1 = True
        #player 2
        else:
            if self.firing2 == True:
                self.firing2 = False
            else:
                self.firing2 = True

    def multiPlayerMove(self, data, num):
        #player 1
        if num == 0:
            #moves the player if he is alive
            if self.player1Lives > 0:
                player1 = self.player1Group.sprites()[0]
                player1.x = data["x"]
                player1.y = data["y"]
        #player 2
        else:
            if self.player2Lives > 0:
                player2 = self.player2Group.sprites()[0]
                player2.x = data["x"]
                player2.y = data["y"]

    def multiUseBomb(self, data, num):
        #player 1
        if num == 0:
            #if the player still has bombs, use one
            if self.player1Bombs > 0:
                self.bombUsed = True
                self.player1Bombs -= 1
        #player 2
        else:
            if self.player2Bombs > 0:
                self.bombUsed = True
                self.player2Bombs -= 1

    def multiMovePlayer(self, keyCode, player):
        #moves the player with keyboard
        if keyCode == pygame.K_LEFT:
            if player.x - player.width/2 > 0:
                player.x -= 10

        if keyCode == pygame.K_RIGHT:
            if player.x + player.width/2 < self.width:
                player.x += 10

        if keyCode == pygame.K_UP:
            if player.y - player.height/2 > 0:
                player.y -= 10

        if keyCode == pygame.K_DOWN:
            if player.y + player.height/2 < self.height:
                player.y += 10

    def multiKeyPressed(self, data, num):
        keyCode = data["keyCode"]
        if num == 0:
            if self.player1Lives > 0:
                player1 = self.player1Group.sprites()[0]
                #alternative way of firing with z key
                if keyCode == pygame.K_z:
                    self.firing1 = True
                #alternative way of using a bomb
                elif keyCode == pygame.K_x:
                    if self.player1Bombs > 0:
                        self.bombUsed = True
                        self.player1Bombs -= 1
                elif keyCode == pygame.K_ESCAPE:
                    self.init()
                self.multiMovePlayer(keyCode, player1)
            if self.isGameOver or self.gameWon == True:
                if keyCode == pygame.K_RETURN:
                    self.init()
        else:
            if self.player2Lives > 0:
                player2 = self.player2Group.sprites()[0]
                #alternative way of firing with z key
                if keyCode == pygame.K_z:
                    self.firing2 = True
                #alternative way of using a bomb
                elif keyCode == pygame.K_x:
                    if self.player2Bombs > 0:
                        self.bombUsed = True
                        self.player2Bombs -= 1
                elif keyCode == pygame.K_ESCAPE:
                    self.init()
                self.multiMovePlayer(keyCode, player2)
            if self.isGameOver or self.gameWon == True:
                if keyCode == pygame.K_RETURN:
                    self.init()
            
    def multiKeyReleased(self, data, num):
        keyCode = data["keyCode"]
        if num == 0:
            player1 = self.player1Group.sprites()[0]
            #alternative way of firing with z key
            if keyCode == pygame.K_z:
                self.firing1 = False
        else:
            player2 = self.player2Group.sprites()[0]
            #alternative way of firing with z key
            if keyCode == pygame.K_z:
                self.firing2 = False

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()