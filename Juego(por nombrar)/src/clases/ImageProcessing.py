#Cambia los nombres no más
import pygame as pg
from pygame import sprite
from pygame.locals import *
import imutils
import math
import cv2 as cv
import numpy as np
from settings import *
def rotate_image(mat, angle):
    """
    Rotates an image (angle in degrees) and expands image to avoid cropping
    """

    height, width, bytes = mat.shape
    image_center = (width/2, height/2) # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape

    rotation_mat = cv.getRotationMatrix2D(image_center, 90 + angle, 1.)

    # rotation calculates the cos and sin, taking absolutes of those.
    abs_cos = abs(rotation_mat[0,0])
    abs_sin = abs(rotation_mat[0,1])

    # find the new width and height bounds
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    # subtract old image center (bringing image back to origo) and adding the new image center coordinates
    rotation_mat[0, 2] += bound_w/2 - image_center[0]
    rotation_mat[1, 2] += bound_h/2 - image_center[1]

    # rotate image with the new bounds and translated rotation matrix
    rotated_mat = cv.warpAffine(mat, rotation_mat, (bound_w, bound_h))

    return rotated_mat
class Shadow(sprite.Sprite):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        try:
            self.rect = self.image.get_rect()
        except:
            self.rect = self.parent.image.get_rect()
    @property
    def array(self):
        return pg.surfarray.pixels3d(self.parent.image if self.rect.y < self.parent.rect.y else pg.transform.flip(self.parent.image,True, False))
    def get_shadow(self, image):
        im_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        (thresh, im_bw) = cv.threshold(im_gray, 0, 255, cv.THRESH_BINARY |  cv.THRESH_TRIANGLE)
        kernel = np.ones((3,3),np.uint8)
        opening = cv.morphologyEx(im_bw,cv.MORPH_OPEN,kernel, iterations = 2)


        sure_bg = cv.dilate(opening, kernel ,iterations = 6)
        dist_transform = cv.distanceTransform(opening,cv.DIST_L2,5)
        ret, sure_fg = cv.threshold(dist_transform,0.7*dist_transform.max(),255,0)
        sure_bg = np.uint8(sure_fg)
        surf = pg.surfarray.make_surface(sure_fg)
        return surf
    @property
    def image(self):
        V_1 = np.array([1, 0])
        V_2 = np.array([self.rect.x-self.parent.rect.centerx, self.rect.y-self.parent.rect.y+self.rect.centery-self.parent.rect.centery])
        V_2 = V_2/np.linalg.norm(V_2)
        rows, cols, bytes = self.array.shape
        angle = math.acos(np.dot(V_2,V_1)) if self.rect.y > self.parent.rect.y else -math.acos(np.dot(V_2,V_1))
        dst = rotate_image(self.array, np.degrees(angle))
        img = self.get_shadow(dst).convert()
        #img.set_colorkey((255,255,255))

        return img

    def update(self):
        self.rect.x, self.rect.y = self.parent.rect.x-6, self.parent.rect.bottom-5
def draw_fog(screen, depth):
    fog = pg.Surface((W,H), pg.SRCALPHA)
    fog.fill((0,0,0,255))
    for i in range(255, 1, -1):
        pg.draw.circle(fog, (0,0,0,i), (W//2,H//2), round(i*depth))
    return fog
