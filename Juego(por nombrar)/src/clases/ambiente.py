import pygame as pg
from pygame import sprite
from itertools import cycle
from pygame.locals import *
import imutils
import math
import cv2 as cv
import numpy as np
from settings import *
from ImageProcessing import *
from glob import glob
class fuenteLuz(pg.sprite.Sprite):
    def __init__(self, imgPath, lightRadius):
        super().__init__()
        self.animations = cycle(pg.image.load(img) for img in glob("animations/{}**".format(imgPath)))
        self.animation_counter = 0
        self.__image = next(self.animations)
        self.rect = self.image.get_rect()
    @property
    def image(self):

        if self.animation_counter > 4:
            self.animation_counter = 0
            self.__image = next(self.animations)
        return self.__image
    def update(self):
        self.animation_counter += 1
    def cast_shadow(self):
        
if __name__ == "__main__":
    clock = pg.time.Clock()
    fire = fuenteLuz("fire/frame", 3)
    pg.init()
    g = pg.sprite.Group()
    g.add(fire)
    screen =  pg.display.set_mode((500,400))
    screen.fill((255,255,255))
    while True:
        for event in pg.event.get():
            if event.type is pg.QUIT:
                pg.quit() # quit the screen
                break
        screen.fill((255,255,255))
        g.update()
        g.draw(screen)
        pg.display.update()
        clock.tick(60)
