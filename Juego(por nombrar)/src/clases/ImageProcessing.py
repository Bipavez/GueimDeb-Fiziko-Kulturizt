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

    rotation_mat = cv.getRotationMatrix2D(image_center,  angle, 1.)

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
class Shadow(sprite.Sprite): #clase base para las sombras, se maneitenen poco tiempo en memoria
    def __init__(self, parent, alpha,  angle):
        super().__init__()
        self.parent = parent
        self.alpha = alpha
        self.angle = angle
        try:
            self.rect = self.image.get_rect() #inútil, reemplazar
        except:
            self.rect = self.parent.image.get_rect()
        w, h, c = pg.surfarray.array3d(self.image).shape
        self.__corrections = [w/2, h/2]
    @property
    def corrections(self):
        w, h, c = pg.surfarray.array3d(self.image).shape
        self.__corrections = [w/2, h/2] #correcciones necesarias para el fijamiento preciso de la sombra en el plano #MalditosRects
        return self.__corrections
    @property
    def array(self):
        return pg.surfarray.pixels3d(self.parent.image if self.rect.y < self.parent.rect.y else pg.transform.flip(self.parent.image,True, False)) #ew, linea larga
    def get_shadow(self, image, alpha):
        im_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY) #se aplica escala de grises a la matriz
        (thresh, im_bw) = cv.threshold(im_gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_TRIANGLE) #se binariza la matriz
        kernel = np.ones((3,3),np.uint8) #kernel de l a transofrmación; puede ser 3x3 ó 5x5
        im_bw = cv.erode(im_bw, kernel ,iterations = 1) #se erosiona la imagen obteniendo una silueta más robusta del personaje
        surf = pg.surfarray.make_surface(im_bw) #creación de superficie pygame
        surf.set_alpha(alpha) #bueno, la transparencia

        return surf
    def rotation(self, angle):
        return rotate_image(self.array, np.degrees(angle)) #para orden, limpiar

    @property
    def image(self):
        dst  = self.rotation(self.angle) #se rota la figura
        img = self.get_shadow(dst, self.alpha).convert() #se convierte la figura para compatibilidad con las operaciones normales de pygame
        img.set_colorkey((255,255,255)) #se hace transparente el blanco
        return img

def draw_fog(size, depth):
    fog = pg.Surface(size, pg.SRCALPHA)
    fog.fill((0,0,0,255))
    for i in range(255, 1, -1): #muy intensivo en recursos, cambiar o encontrar alguna forma de hacerlo mas eficiente (para grandes pantallas)
        pg.draw.circle(fog, (0,0,0,i), (size[0]//2,size[1]//2), round(i*depth))
    return fog
