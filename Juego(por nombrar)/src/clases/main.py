import pygame as pg
from pygame import sprite
from pygame.locals import *
import math

from Control import *
from Sprites import *
from ImageProcessing import *

#GAME DISPLAY PARAMETERS            #Exportar esto a otro archivo
W = 700
H = 500

FOG = 1
#/

player_x = 0
player_y = 0

def draw_fog(screen, depth):
    fog = pg.Surface((W,H), pg.SRCALPHA)
    fog.fill((0,0,0,255))
    for i in range(255, 1, -1):
        pg.draw.circle(fog, (0,0,0,i), (W//2,H//2), round(i*depth))
    return fog

pg.init()
screen = pg.display.set_mode((W,H))
background = pg.image.load("animations\\background.png")

player = Character_Sprite("player", 5)
p_l, p_h = player.rect.width, player.rect.height
player.set_position((W//2 - p_l//2, H//2 - p_h//2)) #Cambiar, limpiar

ball = Item_Sprite("ball", player)

npc = Character_Sprite("player",0)
npc.set_position((400,300))
shadow = Shadow(player)
player_entities = sprite.Group(shadow, player, ball)
background_entities = sprite.Group(npc)
collision_entities = sprite.Group(player, npc)

player_x = player.x
player_y = player.y

clock = pg.time.Clock()

fog = draw_fog(screen, FOG)

while True:
    #Screen filling START
    screen.fill((0,0,0))
    screen.blit(background, (W//2 - player.x, H//2 - player.y, W, H))
    background_entities.draw(background)
    player_entities.draw(screen)
    if FOG != 0:
        screen.blit(fog, (0,0))
    #Screen filling END
        
    keys = pg.key.get_pressed()
    if keys[K_ESCAPE]:
        pg.quit() # quit the screen
        break
    if keys[K_f]:
        FOG = not FOG
        if FOG:
            fog = draw_fog(screen)
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
    pg.display.update()
    background_entities.clear(background,background)
