import pygame as pg
from pygame.locals import *
import math

player_pos = [100,100]

ball = pg.image.load("Juego(por nombrar)/src/clases/animations/ball_1.png")
person = pg.image.load("Juego(por nombrar)/src/clases/animations/player_walk_d1.png")
#hitbox_p = pg.Block((120,120,120), 20, 40)

pg.init()
screen = pg.display.set_mode((500,500))
pg.display.set_caption("hitbox test")

ball.convert()
person.convert_alpha()
person.set_alpha(255)
person.set_colorkey((255, 255, 255))

subrect = person.subsurface([5,0,40,5])
subrect.fill((255,0,0))

t = 0
while True:
    pg.event.pump()
    ky = pg.key.get_pressed()
    if ky[K_ESCAPE]:
        print(pg.display.Info())
        pg.quit()
    if ky[K_DOWN]:
        player_pos[1] += 5
    if ky[K_UP]:
        player_pos[1] -= 5
    if ky[K_LEFT]:
        player_pos[0] -= 5
    if ky[K_RIGHT]:
        player_pos[0] += 5

    screen.fill((255, 255, 255))
    screen.blit(ball, (350,250), (0,0,100,100))
    screen.blit(person, player_pos)

    alpha = 200 +  55*math.sin(t)
    person.set_alpha(alpha)
    print(person.get_alpha())
    #hitbox_p.x
    t += 0.3
    pg.time.delay(50)
    pg.display.update()
