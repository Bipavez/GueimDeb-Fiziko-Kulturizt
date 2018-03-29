
import pygame as pg
from pygame import sprite
from pygame.locals import *

import glob
from itertools import cycle

class Character_Sprite(sprite.Sprite):
    def __init__(self, name, speed):
        super().__init__()
        self.animation_list = self.get_animation_list(name)
        self.animations = {"WALK_D":cycle(self.animation_list["WALK_D"]),
                           "WALK_U":cycle(self.animation_list["WALK_U"]),
                           "WALK_L":cycle(self.animation_list["WALK_L"]),
                           "WALK_R":cycle(self.animation_list["WALK_R"])
                          }
        self.__image = next(self.animations["WALK_D"])
        self.walk_frame = 1
        self.going = "WALK_D"

        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.speed = speed

    def set_position(self, coords):
        self.x,self.y = coords[0], coords[1]
        self.rect.x, self.rect.y = self.x, self.y

    @property
    def image(self):
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
                a.set_colorkey((255,255,255))
        return animation_list

    def move(self):
        pass

    def update(self):
        self.move()



class Item_Sprite(sprite.Sprite):
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
    def update(self):
        self.rect.x = self.parent.rect.x - 20
        self.rect.y = self.parent.rect.y - 20
