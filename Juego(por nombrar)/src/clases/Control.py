import pygame as pg
from pygame import sprite
from pygame.locals import *

def handle_keys(player):
    key = pg.key.get_pressed()
    if key[K_ESCAPE]:
        pg.quit()
        #Thread exit?
    if key[pg.K_s] or key[pg.K_w]:
        player.walk_frame += 1
        if key[pg.K_s]:
            player.going = "WALK_D"
            if player.y <= 1527:
                player.y += player.speed
        if key[pg.K_w]:
            player.going = "WALK_U"
            if player.y > 0:  # up key
                 player.y -= player.speed
    elif key[pg.K_a] or key[pg.K_d]:
        player.walk_frame += 1
        if key[pg.K_d]:
            player.going = "WALK_R"
            if player.x <= 1667: # right key
                 player.x += player.speed
        if key[pg.K_a]:
            player.going = "WALK_L"
            if player.x > 0:  # left key
                 player.x -= player.speed
