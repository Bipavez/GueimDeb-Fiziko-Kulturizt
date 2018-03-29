import pygame as pg
from pygame import sprite
from pygame.locals import *

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
