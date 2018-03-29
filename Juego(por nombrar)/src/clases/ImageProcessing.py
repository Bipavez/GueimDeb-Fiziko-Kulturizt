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
        V_1 = np.array([1, 0])
        V_2 = np.array([self.rect.x-self.parent.rect.x, self.rect.y-self.parent.rect.y])/np.linalg.norm(np.array([self.rect.x-self.parent.rect.x, self.rect.y-self.parent.rect.y]))
        array = pg.surfarray.pixels3d(pg.transform.flip(self.parent.image,True, False) if self.rect.y < self.parent.rect.y else self.parent.image)
        rows, cols, bytes = array.shape
        angle = math.acos(np.dot(V_2,V_1)) if self.rect.y > self.parent.rect.y else -math.acos(np.dot(V_2,V_1))
        print(array.shape)
        print(angle)
        M = cv.getRotationMatrix2D((rows/2+20, cols/2), 90 + np.degrees(angle), 1)
        dst = cv.warpAffine(array, M, (cols+20,rows+20))
        img = pg.surfarray.make_surface(dst)
        img.set_colorkey((0,0,0))
        return img
    def update(self):
        self.rect.y , self.rect.x = (self.parent.rect.y + self.parent.rect.width*math.sin(self.parent.walk_frame*0.07), self.parent.rect.x - self.parent.rect.width*math.cos(self.parent.walk_frame*0.07))
