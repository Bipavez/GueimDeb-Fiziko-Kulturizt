import pygame as pg
from pygame import sprite
from itertools import cycle
from pygame.locals import *
import imutils
import math, random, sys
import cv2 as cv
import numpy as np
from settings import *
from ImageProcessing import *
from glob import glob
def delta(t, x0, x):
    if x == x0:
        return t
    else:
        return t*(math.sin(x)+math.cos(x))
class circle(pg.sprite.Sprite):
    def __init__(self, xy, radius, id, surface):
        super().__init__()
        self.xy = xy
        self.radius = radius
        self.id = id
        self.surface = surface
        self.color = (random.randint(128, 255), random.randint(128, 255),
                random.randint(128, 255), 255) if id != 5 else (255,255,0)
    def hasOverlapped(self, xy, radius):
        minDistance = 0.0 + radius + self.radius
        distance = math.hypot(xy[0] - self.xy[0], xy[1] - self.xy[1])
        if distance >= minDistance: return False

        radians = math.atan2(xy[1] - self.xy[1], xy[0] - self.xy[0])
        overlap = 1 + (minDistance - distance)
        return (math.cos(radians) * overlap, math.sin(radians) * overlap, overlap)
    def setXY(self, xy):
        self.xy = xy
    def draw(self):
        pg.draw.circle(self.surface, self.color, (int(self.xy[0]), int(self.xy[1])), self.radius, 0)
class fuenteLuz(pg.sprite.Sprite):
    def __init__(self, imgPath, lightRadius, lightable):
        super().__init__()
        self.center = (0,0)
        self.x = 300
        self.y = 500
        self.lightable = lightable
        self.lightRadius = lightRadius
        self.shadows = pg.sprite.Group()

        self.animations = cycle(self.get_animations(imgPath))
        self.animation_counter = 0
        self.__image = next(self.animations)
        array = pg.surfarray.array3d(self.__image)
        self.circ = circle(self.__image.get_rect().center, lightRadius, 5, self.__image)
        self.rect = pg.rect.Rect(self.x, self.y, self.x+lightRadius, self.y+ lightRadius)


        self.radius = self.circ.radius

    def get_animations(self, imgPath):
        self.preAnimation = [pg.image.load(img) for img in glob("animations/{}**".format(imgPath))]
        for a in self.preAnimation:
            a.convert()
        self.postAnimation = [pg.surfarray.make_surface(
                               cv.copyMakeBorder(pg.surfarray.array3d(surface),
                                                round(self.lightRadius-sizes[1]/2),
                                                round(self.lightRadius-sizes[1]/2),
                                                round(self.lightRadius-sizes[0]/2),
                                                round(self.lightRadius-sizes[0]/2),
                                                cv.BORDER_ISOLATED)
                                                )
                                for sizes, surface in zip([pg.surfarray.array3d(surf).shape for surf in self.preAnimation],
                                                          self.preAnimation)]
        for a in self.postAnimation:
            a.set_colorkey((0,0,0))
        return self.postAnimation
    @property
    def image(self):

        if self.animation_counter > 4:
            self.animation_counter = 0
            self.__image = next(self.animations)
        return self.__image
    def update(self, x, y):
        self.set_position(x,y)
        self.check_area()

        self.animation_counter += 1
    def set_position(self, CAMERA_X, CAMERA_Y):

        self.rect.x, self.rect.y = self.x-CAMERA_X, self.y-CAMERA_Y
    def check_area(self):
        obj = pg.sprite.spritecollideany(self, self.lightable)

        if obj != None:
            objX = obj.rect.centerx+obj.corrections[0]
            objY = obj.rect.centery+obj.corrections[1]
            Vect = np.array([self.rect.centerx-objX,
                             self.rect.centery-objY
                            ])
            E_1 = np.array([1,0])

            norm = np.linalg.norm(Vect)
            angle = math.acos(np.vdot(E_1, Vect/norm)) if objY < self.rect.centery else -math.acos(np.vdot(E_1, Vect/norm))
            rnorm = int(round(norm))^2
            angleShadow = angle - np.radians(90)
            angle -= np.radians(180)
            angle = -angle
            print(np.degrees(angle), delta(-30, math.pi/4, angle))
            if norm <= self.radius:
                alpha = 50/rnorm*255 if norm != 0 else 0
                shadow = Shadow(obj, alpha, angleShadow)
                xOffset, yOffset = 0, 0
                if angle >= 0 and angle < math.pi/2:
                    xOffset = math.cos(angle)*shadow.corrections[0]+delta(-15, math.pi/4, angle)
                    yOffset = math.cos(angle)*shadow.corrections[1]+delta(-15, math.pi/4, angle)
                d = pg.display.get_surface()

                d.blit(shadow.image, (obj.rect.x + xOffset , obj.rect.y + yOffset))
                d.blit(obj.image, (obj.rect.x, obj.rect.y))

                del shadow



    def draw(self, surface, point):
        x, y = point
        surface.blit(self, (x+self.w/2, y+h/2))

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
