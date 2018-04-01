
import pygame as pg
from pygame import sprite
from pygame.locals import *

import glob
from itertools import cycle

class Character_Sprite(sprite.Sprite):
    def __init__(self, name, speed):
        super().__init__()
        self.animation_list = self.get_animation_list(name)
        self.animations = {"WALK_D":cycle(self.animation_list["WALK_D"]), #diccionario de animaciones
                           "WALK_U":cycle(self.animation_list["WALK_U"]),
                           "WALK_L":cycle(self.animation_list["WALK_L"]),
                           "WALK_R":cycle(self.animation_list["WALK_R"])
                          }
        self.__image = next(self.animations["WALK_D"])
        self.walk_frame = 1                                            #contador de caminata, en el futuro cambiar para que el jugador no se quede pegado en una sola animación incomoda
        self.going = "WALK_D"
        imageRect = self.image.get_rect()
        self.rect = imageRect
        shape  = pg.surfarray.array3d(self.__image).shape
        w, h , c = shape
        self.corrections = (0,h/2)                                     #correcciones necesarias para la buena referencia de las coordenadas del personaje
        self.x = 0
        self.y = 0
        self.speed = speed
        self.radius = self.rect.width/8
    def set_position(self, CAMERA_X, CAMERA_Y):
        self.rect.x, self.rect.y = self.x-CAMERA_X, self.y-CAMERA_Y
    @property
    def image(self):                                                   #propiedad de la imagen. cambia con un ciclo dependiendo el walk_frame
        if self.__image not in self.animation_list[self.going]:
            self.__image = next(self.animations[self.going])
            self.walk_frame = 1
        else:
            if self.walk_frame % 6 == 0:            #Ajustar el número con FPS
                self.__image = next(self.animations[self.going])
                self.walk_frame += 1
            else:
                pass
        return self.__image

    def get_animation_list(self,name):
        animation_list = {"WALK_U":[pg.image.load(ld_img).convert() for
                           ld_img in glob.glob("animations\\{}\\walk_u*".format(name))],
                           "WALK_D":[pg.image.load(ld_img).convert() for
                           ld_img in glob.glob("animations\\{}\\walk_d*".format(name))],
                           "WALK_L":[pg.image.load(ld_img).convert() for
                           ld_img in glob.glob("animations\\{}\\walk_l*".format(name))],
                           "WALK_R":[pg.image.load(ld_img).convert() for
                           ld_img in glob.glob("animations\\{}\\walk_r*".format(name))]
                           }
        for key in animation_list:                          #Hace el blanco transparente
            for a in animation_list[key]:
                a.set_colorkey((0,0,0))
        return animation_list

    def move(self): #implementar
        pass

    def update(self, CAMERA_X, CAMERA_Y):
        self.move()
        self.set_position(CAMERA_X, CAMERA_Y)



class Item_Sprite(sprite.Sprite):       #Rehacer i think, yo también pienso lo mismo
    def __init__(self, img_pth, parent, speed = 30):
        super().__init__()
        self.speed = speed
        self.animation_list = {"BALL_MOVE":[pg.image.load(ld_img) for ld_img in glob.glob("animations\\{}\\**".format(img_pth))]}
        self.animations = {"BALL_MOVE":cycle(self.animation_list["BALL_MOVE"])}
        self.__image = next(self.animations["BALL_MOVE"])
        self.parent = parent
        self.__animation_count = 0
        self.rect = self.image.get_rect()

    @property
    def animation_count(self):
        self.__animation_count += self.speed
        return self.__animation_count
    @property
    def image(self):
        if self.animation_count % 50 == 0 and self.animation_count != 0:
            self.__animation_count = 0
            self.__image = next(self.animations["BALL_MOVE"])
            return self.__image
        else:
            return self.__image
    def update(self, CAMERA_X, CAMERA_Y):
        self.rect.x = self.parent.rect.x - 20
        self.rect.y = self.parent.rect.y - 20
