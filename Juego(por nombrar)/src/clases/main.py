import pygame as pg
from pygame import sprite
from pygame.locals import *
import time
import math

from Control import *       #En algún momento poner referencias
from Sprites import *
from ImageProcessing import *
from settings import *

<<<<<<< HEAD
FOG = 1
=======
#Start settings
FOG = 0         #Massive lag?
##
>>>>>>> da1c1660b391dfd808f5266295cd1a6f11e0db94


pg.init()
screen = pg.display.set_mode((W,H))
background = pg.image.load("animations\\background.png")
player = Character_Sprite("player", 5)
p_l, p_h = player.rect.width, player.rect.height
player.x, player.y = W//2 - p_l//2, H//2 - p_h//2 #Cambiar, limpiar

ball = Item_Sprite("ball", player)
npc = Character_Sprite("player",0)
npc.x, npc.y = 400,300
shadow = Shadow(player)
player_entities = sprite.Group(shadow, player, ball)
background_entities = sprite.Group(npc)
collision_entities = sprite.Group(player, npc)

CAMERA_X = player.x - W//2 + p_l//2
CAMERA_Y = player.y - H//2 + p_h//2

clock = pg.time.Clock()

if FOG != 0:
    fog = draw_fog((W,H), FOG)

while True:
    #Screen filling
    screen.fill((0,0,0))
    screen.blit(background, (-CAMERA_X,-CAMERA_Y, W, H))
    background_entities.draw(screen)
    player_entities.draw(screen)
    if FOG != 0:
        screen.blit(fog, (0,0))
    ##

    #Event handling
    handle_keys(player)
    for event in pg.event.get():
        if event.type is pg.QUIT:
            pg.quit() # quit the screen
            break
    ##

    player_entities.update(CAMERA_X, CAMERA_Y)
    background_entities.update(CAMERA_X, CAMERA_Y)

    clock.tick(40)
    pg.display.set_caption("{}".format(clock.get_fps()))

    CAMERA_X = player.x - W//2 + p_l//2
    CAMERA_Y = player.y - H//2 + p_h//2
    pg.display.update()
