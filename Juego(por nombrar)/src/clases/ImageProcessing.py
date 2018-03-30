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
        array = pg.surfarray.pixels3d(self.parent.image if self.rect.y < self.parent.rect.y else pg.transform.flip(self.parent.image,True, False))
        rows, cols, bytes = array.shape
        angle = math.acos(np.dot(V_2,V_1)) if self.rect.y > self.parent.rect.y else -math.acos(np.dot(V_2,V_1))
        maxWH = max(rows, cols)
        M = cv.getRotationMatrix2D((maxWH/2, maxWH/2), 90 + np.degrees(angle), 1)
        dst = cv.warpAffine(array, M, (cols+20,rows+30))
        """
        gray = cv.cvtColor(array,cv.COLOR_BGR2GRAY)
        _,thresh = cv.threshold(gray,1,255,cv.THRESH_BINARY)
        contours,hierarchy, something = cv.findContours(thresh,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        cnt = contours[0]
        x,y,w,h = cv.boundingRect(cnt)
        dst = dst[y:y+h,x:x+w]
        """
        img = pg.surfarray.make_surface(dst)
        img.set_colorkey((0,0,0))

        return img
    def update(self):
        xOffset = self.parent.rect.width*math.sin(self.parent.walk_frame*0.07)
        yOffset = self.parent.rect.width*math.cos(self.parent.walk_frame*0.07)
        self.rect.center = (self.rect.centerx + xOffset, self.rect.centery +yOffset)
        self.rect.x , self.rect.y = (self.parent.rect.x + xOffset, self.parent.rect.y + yOffset)
