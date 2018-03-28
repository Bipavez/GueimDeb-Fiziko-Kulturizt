import pygame as pg
from pygame.locals import *
import math

pg.init()
size = (400, 400)
screen = pg.display.set_mode(size)
#Este test es tan raro por el formato de la imagen ball. El otro funciona con el
#alpha sin problemas. Habrá que ver supongo
ball = pg.image.load("Juego(por nombrar)/src/clases/animations/ball_1.png")
ball.convert()
ball.convert_alpha()        #No creo que necesario

t = 0
while True:
    pg.event.pump()
    for event in pg.event.get():
        if event.type == KEYDOWN and event.key == K_ESC:
            pg.quit()

    alpha = round(55*math.sin(t)+200)
    new = ball.copy()
    new.fill((255, 255, 255, alpha), None, pg.BLEND_RGBA_MULT)
    t += 0.3

    screen.fill([0,0,255])
    pg.draw.rect(screen, [0,255,0], [100,100,200,200], 0)
    screen.blit(new, [185,185])

    pg.time.delay(100)
    pg.display.update()
