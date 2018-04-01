import pygame as pg
from pygame import sprite
from pygame.locals import *
import imutils
import math
import cv2 as cv
import numpy as np
from settings import *
from ImageProcessing import *
class fuenteLuz(pg.sprite.Sprite):
    def __init__(self, imgPath, lightRadius):
        super().__init__()
        self.animations = {}
