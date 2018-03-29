import pygame
from pygame import sprite
from pygame.locals import *
import glob
from itertools import cycle
import threading
import sys, os
import time
import numpy
window_up = 720
window_len = 1080
class Player_Sprite(pygame.sprite.Sprite):
    def __init__(self,win_h  ,win_l ,img_pth = "player",speed  = 1
                 , width = 64, height = 64, animation_speed = 3.5):
        """Clase para jugadores,  y posiblemente NPCs,
           img_pth es el nombre inicial de los archivos que contienen las animaciones,
           así es facil inicializar los personajes,  speed se refiere a la velocidad
           con la cual el personaje avanza, 1 es bastante rápido, cambiar a futuro;
           animation_speed es la velocidad de las animaciones(por ahora de mov),
           esta se comporta como 1/x y es más rápida a la mayor cantidad."""
        super().__init__()
        self.animation_speed = int(100/animation_speed) if animation_speed != 0 else 23
        self.speed = speed
        self.animation_list = {"WALK_U":[pygame.image.load(ld_img) for
                               ld_img in glob.glob("animations\\{}\\walk_u*".format(img_pth))],
                               "WALK_D":[pygame.image.load(ld_img) for
                               ld_img in glob.glob("animations\\{}\\walk_d*".format(img_pth))],
                               "WALK_L":[pygame.image.load(ld_img) for
                               ld_img in glob.glob("animations\\{}\\walk_l*".format(img_pth))],
                               "WALK_R":[pygame.image.load(ld_img) for
                               ld_img in glob.glob("animations\\{}\\walk_r*".format(img_pth))]
                              }
        self.animations = {"WALK_D":cycle(self.animation_list["WALK_D"]),
                           "WALK_U":cycle(self.animation_list["WALK_U"]),
                           "WALK_L":cycle(self.animation_list["WALK_L"]),
                           "WALK_R":cycle(self.animation_list["WALK_R"])
                          }
        self.__image = next(self.animations["WALK_D"])
        self.distanceMoved = [0,0]
        self.win_l = win_l
        self.win_h = win_h
        self.y = 0
        self.x = 0
        self.going = ""
        self.rect = self.image.get_rect()
        self.set_position((win_l/2, win_h/2))
    @property
    def image(self):
        if self.going == "l" and self.__image not in self.animation_list["WALK_L"]:
            self.__image = self.animation_list["WALK_L"][0]
        if self.going == "r" and self.__image not in self.animation_list["WALK_R"]:
            self.__image = self.animation_list["WALK_R"][0]
        if self.going == "u" and self.__image not in self.animation_list["WALK_U"]:
            self.__image = self.animation_list["WALK_U"][0]
        if self.going == "d" and self.__image not in self.animation_list["WALK_D"]:
            self.__image = self.animation_list["WALK_D"][0]
        if (self.distanceMoved[1] % self.animation_speed == 0 and self.distanceMoved[1] != 0):
            if self.distanceMoved[1] < 0:
                self.distanceMoved[1] = -1
                self.__image = next(self.animations["WALK_L"])
            elif self.distanceMoved[1] > 0:
                self.distanceMoved[1] = 1
                self.__image = next(self.animations["WALK_R"])
        if (self.distanceMoved[0] % self.animation_speed == 0 and self.distanceMoved[0] != 0):
            if self.distanceMoved[0] < 0:
                self.distanceMoved[0] = -1
                self.__image = next(self.animations["WALK_U"])
            elif self.distanceMoved[0] > 0:
                self.distanceMoved[0] = 1
                self.__image = next(self.animations["WALK_D"])
        else:
            pass
        return self.__image
    def set_position(self, coords):
        self.x,self.y = coords[0], coords[1]
        self.rect.x,self.rect.y = self.x, self.y
    def handle_keys(self): #como se manejan las acciones, en un futuro añadir ataque y defensa
        key = pygame.key.get_pressed()
        vel = self.speed
        if key[pygame.K_DOWN] or key[pygame.K_UP]:
            if key[pygame.K_DOWN]:
                self.going = "d"
                if self.rect.y <= self.win_h:
                    self.distanceMoved[0] += vel #
                    self.rect.move_ip(0,vel)
                else:
                    self.distanceMoved[0] = 0
            if key[pygame.K_UP]:
                self.going = "u"
                if self.rect.y >= 0:# up key
                    self.distanceMoved[0] -= vel
                    self.rect.move_ip(0, -vel) # move up
                else:
                    self.distanceMoved[0] = 0
        elif key[pygame.K_LEFT] or key[pygame.K_RIGHT]:
            if key[pygame.K_RIGHT]:
                self.going = "r"
                if self.rect.x <= self.win_l: # right key
                    self.distanceMoved[1] += vel
                    self.rect.move_ip(vel,0) # move right
                else:
                    self.distanceMoved[1] = 0
            if key[pygame.K_LEFT]:
                self.going = "l"
                if self.rect.x >= 0: # left key
                    self.distanceMoved[1] -= 1
                    self.rect.move_ip(-vel,0) # move left
                else:
                    self.distanceMoved[1] = 0
    def update(self):
        self.handle_keys()
class Equipment(pygame.sprite.Sprite):
    def __init__(self, img_pth, parent):
        super().__init__()
        self.animation_list = {"BALL_MOVE":[pygame.image.load(ld_img) for ld_img in glob.glob("animations\\{}\\**".format(img_pth))]}
        self.animations = {"BALL_MOVE":cycle(self.animation_list["BALL_MOVE"])}
        self.__image = next(self.animations["BALL_MOVE"])
        print(self.animation_list)
        self.parent = parent
        self.__animation_count = 0
        self.rect = self.image.get_rect()
    @property
    def animation_count(self):
        self.__animation_count += 1
        return self.__animation_count
    @property
    def image(self):
        if self.animation_count % 50 == 0 and self.animation_count != 0:
            self.__animation_count = 1
            self.__image = next(self.animations["BALL_MOVE"])
            return self.__image
        else:
            return self.__image
    def update(self):
        self.rect.x = self.parent.rect.x - 20
        self.rect.y = self.parent.rect.y - 20
pygame.init()
screen = pygame.display.set_mode((window_len, window_up), RESIZABLE | FULLSCREEN)
PJ = Player_Sprite(window_up-64, window_len-50)
Ball = Equipment("ball", PJ) # create an instance
clock = pygame.time.Clock()
KEYESC = pygame.K_q
running = True
Keys = set([pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT])
G = pygame.sprite.Group()
G.add(PJ)
G.add(Ball)
sec_screen = pygame.surface.Surface((window_len, window_up))

while running:
    # handle every event since the last frame.
    for event in pygame.event.get():
        print(event)
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            pygame.quit() # quit the screen
            running = False
        if event.type == pygame.QUIT or event.type == KEYESC:
                pygame.quit() # quit the screen
                running = False
        if pygame.key.get_pressed()[pygame.K_f]:
            if "1920" in str(pygame.display.Info()):
                window_up = 900
                window_len = 1600
                pygame.transform.scale(sec_screen,(window_len, window_up))
                pygame.display.set_mode((window_len,window_up))
                pygame.display.update()

            else:
                window_up = 720
                window_len = 1080
                pygame.transform.scale(sec_screen, (window_len, window_up))
                pygame.display.set_mode((window_len,window_up), FULLSCREEN)
                pygame.display.update()
    G.update()

     # handle the keys
    sec_screen.fill((255,255,255))
     # fill the screen with white
     # draw the bird to the screen
    G.draw(sec_screen)
    screen.blit(sec_screen, (0,0))

    pygame.display.update() # update the screen

    clock.tick(40)
