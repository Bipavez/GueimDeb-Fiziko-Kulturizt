#Cambia los nombres no más
import pygame as pg
from pygame import sprite
from pygame.locals import *

import math
import cv2 as cv
import numpy as np

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
