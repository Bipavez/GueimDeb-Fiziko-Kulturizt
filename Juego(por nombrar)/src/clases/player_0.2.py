import pygame as pg
from pygame import sprite
from pygame.locals import *
import math
import cv2 as cv
import numpy as np
import glob
from itertools import cycle

win_l = 700
win_h = 500

player_x = 0
player_y = 0

class Character_Sprite(sprite.Sprite):
    def __init__(self, name, speed):
        super().__init__()
        self.animation_list = self.get_animation_list(name)
        self.animations = {"WALK_D":cycle(self.animation_list["WALK_D"]),
                           "WALK_U":cycle(self.animation_list["WALK_U"]),
                           "WALK_L":cycle(self.animation_list["WALK_L"]),
                           "WALK_R":cycle(self.animation_list["WALK_R"])
                          }
        self.__image = next(self.animations["WALK_D"])
        self.walk_frame = 1
        self.going = "WALK_D"

        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.speed = speed

    def set_position(self, coords):
        self.x,self.y = coords[0], coords[1]
        self.rect.x, self.rect.y = self.x, self.y

    @property
    def image(self):
        if self.__image not in self.animation_list[self.going]:
            self.__image = next(self.animations[self.going])
            self.walk_frame = 1
        else:
            if self.walk_frame % 6 == 0:            #Ajustar el número con FPS
                self.__image = next(self.animations[self.going])
                self.walk_frame += 1
            else:
                pass
        return self.__image

    def get_animation_list(self,name):
        animation_list = {"WALK_U":[pg.image.load(ld_img).convert() for
                           ld_img in glob.glob("animations\\{}\\walk_u*".format(name))],
                           "WALK_D":[pg.image.load(ld_img).convert() for
                           ld_img in glob.glob("animations\\{}\\walk_d*".format(name))],
                           "WALK_L":[pg.image.load(ld_img).convert() for
                           ld_img in glob.glob("animations\\{}\\walk_l*".format(name))],
                           "WALK_R":[pg.image.load(ld_img).convert() for
                           ld_img in glob.glob("animations\\{}\\walk_r*".format(name))]
                           }
        for key in animation_list:                          #Hace el blanco transparente
            for a in animation_list[key]:
                a.set_colorkey((255,255,255))
        return animation_list

    def move(self):
        pass

    def update(self):
        self.move()



class Item_Sprite(sprite.Sprite):
    def __init__(self, img_pth, parent, speed = 30):
        super().__init__()
        self.speed = speed
        self.animation_list = {"BALL_MOVE":[pg.image.load(ld_img) for ld_img in glob.glob("animations\\{}\\**".format(img_pth))]}
        self.animations = {"BALL_MOVE":cycle(self.animation_list["BALL_MOVE"])}
        self.__image = next(self.animations["BALL_MOVE"])
        self.parent = parent
        self.__animation_count = 0
        self.rect = self.image.get_rect()

    @property
    def animation_count(self):
        self.__animation_count += self.speed
        return self.__animation_count
    @property
    def image(self):
        if self.animation_count % 50 == 0 and self.animation_count != 0:
            self.__animation_count = 0
            self.__image = next(self.animations["BALL_MOVE"])
            return self.__image
        else:
            return self.__image
    def update(self):
        self.rect.x = self.parent.rect.x - 20
        self.rect.y = self.parent.rect.y - 20

def handle_keys(player):
    key = pg.key.get_pressed()
    vel = player.speed
    if key[pg.K_DOWN] or key[pg.K_UP]:
        player.walk_frame += 1
        if key[pg.K_DOWN]:
            player.going = "WALK_D"
            if player.y <= 1527:
                player.y += player.speed
        if key[pg.K_UP]:
            player.going = "WALK_U"
            if player.y > 0:  # up key
                 player.y -= player.speed
    elif key[pg.K_LEFT] or key[pg.K_RIGHT]:
        player.walk_frame += 1
        if key[pg.K_RIGHT]:
            player.going = "WALK_R"
            if player.x <= 1667: # right key
                 player.x += player.speed
        if key[pg.K_LEFT]:
            player.going = "WALK_L"
            if player.x > 0:  # left key
                 player.x -= player.speed
class Shadow(sprite.Sprite):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        try:
            self.rect = self.image.get_rect()
        except:
            self.rect = self.parent.image.get_rect()
    @property
    def image(self):
        xProy = self.rect.x + self.parent.rect.x
        dist = math.sqrt(xProy**2+(self.rect.y+self.parent.rect.y)**2)
        array = pg.surfarray.pixels3d(self.parent.image)
        rows, cols, bytes = array.shape
        M = cv.getRotationMatrix2D((rows/2+20, cols/2), 90 + math.acos(xProy/dist), 1)
        M = np.flip(M, axis=0)
        dst = cv.warpAffine(array, M, (cols+20,rows+20))
        img = pg.surfarray.make_surface(dst)
        return img
    def update(self):
        self.rect.y , self.rect.x = (self.parent.rect.y + 0.1*self.parent.rect.width*math.sin(self.parent.walk_frame*0.1),self.parent.rect.x + 0.1*self.parent.rect.width*math.sin(self.parent.walk_frame*0.1))





pg.init()
screen = pg.display.set_mode((win_l,win_h))
background = pg.image.load("animations\\background.png")

player = Character_Sprite("player", 5)
p_l, p_h = player.rect.width, player.rect.height
player.set_position((win_l//2 - p_l//2, win_h//2 - p_h//2)) #Cambiar, limpiar

ball = Item_Sprite("ball", player)

npc = Character_Sprite("player",0)
npc.set_position((400,300))
shadow = Shadow(player)
player_entities = sprite.Group(shadow ,player, ball)
background_entities = sprite.Group(npc)

player_x = player.x
player_y = player.y

clock = pg.time.Clock()

while True:
    screen.fill((0,0,0))
    screen.blit(background, (win_l//2 - player.x, win_h//2 - player.y, win_l, win_h))
    background_entities.draw(background)
    player_entities.draw(screen)

    if pg.key.get_pressed()[pg.K_ESCAPE]:
        pg.quit() # quit the screen
        break
    for event in pg.event.get():
        if event.type is pg.QUIT:
            pg.quit() # quit the screen
            break

    player_entities.update()
    background_entities.update()

    clock.tick(40)
    pg.display.set_caption("{}".format(clock.get_fps()))

    handle_keys(player)
    player_x = player.x
    player_y = player.y
    print("{}, {}".format(player_x, player_y))
    pg.display.update()
    background_entities.clear(background,background)
