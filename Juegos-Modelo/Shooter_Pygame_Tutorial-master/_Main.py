import pygame

import BasicEnemy
import utils
from GenericPlayer import PlayerActive, Objective
from ClickableRect import TextButton
from backgroundMap import gameMap

pygame.init()

class Tutorial_Game():
    def __init__(self):

        self.gw = pygame.display.set_mode((1000, 600))                  #Create the game window, set up
        pygame.display.set_caption("Pygame Tutorial")
        self.clock = pygame.time.Clock()

        self.enemies = BasicEnemy.Enemy.enemies

        self.player = PlayerActive()                                            #The player object
        self.objv = Objective()
        self.scoreB = utils.ScoreBoard(self.gw)
        self.map = gameMap()

        self.FPS = 30

    def quitGame(self):
        pygame.quit()
        quit()

    def gotoMenu(self):
        rect = self.gw.get_rect()

        def startPlay():
            self.menu = False


        playB = TextButton((rect.centerx, rect.centery-50), (200, 80), utils.green, "Play", startPlay)
        quitB = TextButton((rect.centerx, rect.centery+50), (200, 80), utils.red, "Quit", self.quitGame)

        self.menu = True
        while self.menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitGame()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        menu = False

                self.gw.fill(utils.white)

                text = utils.getFont(size=82, style="bold").render("Tutorial Game", True, utils.black)
                textRect = text.get_rect()
                textRect.center = self.gw.get_rect().center
                textRect.y -= 200
                self.gw.blit(text, textRect)

                playB.update(self.gw)
                quitB.update(self.gw)

                pygame.display.update()
                self.clock.tick(self.FPS)

    def pause(self):
        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        print "game unpaused"
                        pause = False

                text = utils.getFont(size=96, style="bold").render("Paused", True, utils.black)
                textRect = text.get_rect()
                textRect.center = self.gw.get_rect().center

                self.gw.blit(text, textRect)

                pygame.display.update()
                self.clock.tick(self.FPS)

    def playGame(self):
        self.gotoMenu()

        gameActive = True
        while gameActive:                                                  #Game loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameActive = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        print "game Paused"
                        self.pause()


            activeKey = pygame.key.get_pressed()                           #Events for key presses
            if activeKey[pygame.K_RIGHT]:
                self.player.move(1, 0)
            if activeKey[pygame.K_LEFT]:
                self.player.move(-1, 0)
            if activeKey[pygame.K_UP]:
                self.player.move(0, -1)
            if activeKey[pygame.K_DOWN]:
                self.player.move(0, 1)
            if activeKey[pygame.K_SPACE]:
                self.player.doObjective(self.objv)

            cur = pygame.mouse.get_pos()
            mouse = pygame.mouse.get_pressed()                             #Events for mouse presses

            self.gw.fill(utils.white)
            self.map.resetMap()

            if mouse[0]:                                                   #Left-Click events
                self.player.shoot((cur[0] - self.map.offsetX, cur[1] - self.map.offsetY))

            #COLLISION DETECTION
            playerCollisions = pygame.sprite.spritecollide(self.player, self.enemies, False)
            for enemy in playerCollisions:                                 #Enemy-to-player collisions
                enemy.destroy()
                self.player.takeDamage()

            bulletCollision = pygame.sprite.groupcollide(self.enemies, self.player.bullets, False, True)
            for enemy in bulletCollision:                                  #Enemy-to-bullet collisions
                enemy.takeDamage()

            objvCollision = pygame.sprite.spritecollide(self.objv, self.player.bullets, False)
            if self.objv.winMessage != self.objv.displayMessage:
                for bullet in objvCollision:
                    tempLett = self.objv.winMessage[len(self.objv.displayMessage)]
                    if tempLett.upper() == bullet.name:
                        self.objv.displayMessage += tempLett
                        self.objv.redraw()
                        bullet.destroy()
                        if self.objv.winMessage != self.objv.displayMessage:
                            if self.objv.winMessage[len(self.objv.displayMessage)] == " ":
                                self.objv.displayMessage += " "

            #Spawning
            BasicEnemy.spawn()
            #Updates
            self.player.update(self.map.activeMap)
            self.enemies.update(self.player)
            self.objv.update(self.map.activeMap)

            #Drawing
            self.enemies.draw(self.map.activeMap)

            #END drawing stuff
            self.map.update(self.gw, self.player.rect)

            #UI Stuff
            self.scoreB.update(self.gw)

            pygame.display.update()
            self.clock.tick(self.FPS)

        self.quitGame()

game = Tutorial_Game()
game.playGame()
