import math
import random

import pygame

import utils

spawnCD = 0
spawnCDMax = 300

def spawn():
    global spawnCD, spawnCDMax

    spawnCD -= 1
    if spawnCD <= 0:
        newEnemy = Enemy()
        Enemy.enemies.add(newEnemy)

        newEnemy.rect.x = random.randrange(-100, -50)
        newEnemy.rect.y = random.randrange(-50, 650)

        spawnCD = spawnCDMax

class Enemy(pygame.sprite.Sprite):

    enemies = pygame.sprite.Group()

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((50, 50))
        self.image.fill(utils.red)
        self.rect = self.image.get_rect()

        self.speed = 3

        self.cd = 30
        self.cdMax = 30

        Enemy.enemies.add(self)

        self.maxHP = 10.0
        self.HP = self.maxHP

        self.hbWidth = 40
        self.hbHeight = 8
        self.hbBase = pygame.Surface((self.hbWidth, self.hbHeight))


    def stalkPlayer(self, player):

        xdiff = (player.rect.x + player.rect.width/2) - self.rect.x + self.rect.width/2
        ydiff = (player.rect.y + player.rect.height/2) - self.rect.y + self.rect.height/2

        magnitude = math.sqrt(float(xdiff ** 2 + ydiff ** 2))           #Hypotenus distance from player to enemy
        numFrames = int(magnitude / self.speed)                         #Number of frames needed to travel

        xmove = xdiff/numFrames
        ymove = ydiff/numFrames


        self.rect.x += xmove
        self.rect.y += ymove

    def drawHB(self):
        width = int((self.HP / self.maxHP) * self.hbWidth)

        hb = pygame.Surface((width, self.hbHeight))
        hb.fill(utils.green)

        self.hbBase.fill(utils.red)
        self.hbBase.blit(hb, (0,0))

        self.image.blit(self.hbBase, (5, 38))

    def takeDamage(self):                                               #POST: Lose HP, if at 0, die
        self.HP -= 1
        self.drawHB()
        if self.HP <= 0:
            self.destroy()

    def destroy(self):                                                  #POST: Kill this enemy
        self.kill()
        utils.ScoreBoard.enemiesKilled += 1

    def update(self, player):
        self.stalkPlayer(player)