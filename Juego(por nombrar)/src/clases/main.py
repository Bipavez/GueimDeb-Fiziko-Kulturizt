import pygame as pg
from pygame import sprite
from pygame.locals import *
import math

from Control import *
from Sprites import *
from ImageProcessing import *

win_l = 700
win_h = 500

player_x = 0
player_y = 0

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
