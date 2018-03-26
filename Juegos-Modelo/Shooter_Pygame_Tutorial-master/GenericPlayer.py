import math
import random

import pygame

import utils

pygame.init()

#PlayerActive class is the primary player of the game, this is the unit that is being controlled by the user
class PlayerActive(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((100, 100))
        self.image.fill(utils.blue)
        self.rect = self.image.get_rect()

        self.rect.x = 450
        self.rect.y = 250
        self.speed = 5
        self.lives = 30
        utils.ScoreBoard.playerLives = self.lives

        self.spawnDelay = 0                                     #The delay that spawns a new ammunition unit
        self.spawnDelayMax = 15
        self.ammo = pygame.sprite.Group()                       #Ammunition array
        self.bullets = pygame.sprite.Group()                    #Projectile array

        self.cd = 10                                            #Coolddown that represents firerate
        self.cdMax = 10
        self.isAlive = True

        self.objvCounter = 0
        self.objvCounterMax = 15

    def move(self, xdir, ydir):                                 #POST: Move the player from input controls
        self.rect.x += xdir*self.speed
        self.rect.y += ydir*self.speed

    def spawnAmmo(self):                                        #POST: Spawn a new ammunition unit
        self.ammo.add(Bullet())
        utils.ScoreBoard.playerAmmo = len(self.ammo)

    def moveAmmo(self):                                         #POST: Causes the ammo to move inside of the player obj
        self.image.fill(utils.blue)

        for obj in self.ammo:

            if obj.rect.x + obj.rect.width >= self.rect.width:
                obj.xmove *= -1
            elif obj.rect.x <= 0:
                obj.xmove *= -1
            if obj.rect.y + obj.rect.height >= self.rect.height:
                obj.ymove *= -1
            elif obj.rect.y <= 0:
                obj.ymove *= -1

            obj.rect.x += obj.xmove
            obj.rect.y += obj.ymove

            self.image.blit(obj.image, obj.rect)

    def shoot(self, targ):                                      #POST: Fires an ammunition unit toward the mouse
        if self.cd <= 0 and self.ammo:
            self.cd = self.cdMax
            bullet = self.ammo.sprites()[0]                     #Take bullets out in FIFO order
            self.ammo.remove(bullet)

            bullet.rect.x = self.rect.x + self.rect.width/2 - bullet.rect.width/2
            bullet.rect.y = self.rect.y + self.rect.height/2 - bullet.rect.height/2

            bullet.setTarg(targ)
            self.bullets.add(bullet)

    def doObjective(self, objv):

        if self.objvCounter < -30:
            objv.charPos = len(objv.displayMessage)

        if self.objvCounter <= 0 and objv.displayMessage != objv.winMessage:
            self.objvCounter = self.objvCounterMax
            tempLett = objv.winMessage[objv.charPos]
            if tempLett == " ":
                objv.charPos += 1
                return
            for shot in self.ammo:
                if shot.name == tempLett.upper():
                    self.ammo.remove(shot)
                    shot.rect.x = self.rect.x + 25
                    shot.rect.y = self.rect.y + 25
                    shot.setTarg((objv.rect.x + objv.rect.width/2, objv.rect.y + objv.rect.height/2))
                    self.bullets.add(shot)
                    objv.charPos += 1
                    return

    def takeDamage(self):
        self.lives -= 1
        utils.ScoreBoard.playerLives = self.lives

        if self.lives <= 0:
            self.destroy()

    def destroy(self):
        self.isAlive = False

    def update(self, gw):

        if self.isAlive:
            self.cd -= 1
            self.spawnDelay -= 1
            if self.spawnDelay <= 0:
                self.spawnAmmo()
                self.spawnDelay = self.spawnDelayMax

            self.moveAmmo()                                        #NOTE: This function also draws the ammo to the player


            gw.blit(self.image, self.rect)

            self.bullets.update()
            self.bullets.draw(gw)

            self.objvCounter -= 1



#charList = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()
charList = "I F T H I S".split()

#A bullet is a general projectile that is used to destroy enemies as well as complete the objective
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.name = random.choice(charList)
        self.image = utils.getFont(size=26, style='bold').render(self.name, True, utils.black)
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(0, 100 - self.rect.width)
        self.rect.y = random.randint(0, 100 - self.rect.height)

        self.xmove = random.choice([-1, 1])
        self.ymove = random.choice([-1, 1])
        self.speed = 20.0

    def setTarg(self, target):                                       #POST: Assigns the bullet a target in the world
        xdiff = target[0] - self.rect.x - self.rect.width/2
        ydiff = target[1] - self.rect.y - self.rect.height/2

        magnitude = math.sqrt(float(xdiff ** 2 + ydiff ** 2))        #Magnitude of the hypotenuse for travel
        numFrames = 1 + int(magnitude / self.speed)                      #Number of frames the bullet must travel

        self.xmove = xdiff/numFrames
        self.ymove = ydiff/numFrames

        xtravel = self.xmove * numFrames
        ytravel = self.ymove * numFrames

        self.rect.x += xdiff - xtravel
        self.rect.y += ydiff - ytravel

    def destroy(self):
        self.kill()

    def checkDist(self):
        if self.rect.x < -100 or self.rect.x > 2200:
            self.destroy()
        if self.rect.y < -100 or self.rect.y > 2200:
            self.destroy()

    def update(self):
        self.checkDist()
        self.rect.x += self.xmove
        self.rect.y += self.ymove


class Objective():
    def __init__(self):
        self.winMessage = "i i i i i i"
        self.displayMessage = ""
        self.charPos = 0
        self.image = pygame.Surface((80, 80))
        self.redraw()

    def redraw(self):
        self.image.fill(utils.green)

        elements = [str(len(self.displayMessage)), "of", str(len(self.winMessage))]

        for i, string in enumerate(elements):
            self.text = utils.getFont().render(string, True, utils.black)
            self.image.blit(self.text, (20, 5 + i*22))


        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 500

    def update(self, gw):
        gw.blit(self.image, self.rect)
