window_up = 640
window_len = 1080
import glob
import pygame
from itertools import cycle

class Entity:
    def __init__(self, *args, **kwargs):
        self.__HP = HP
        self.name = name
        self.__isAlive = bool()
    @property
    def HP(self):
        return self.__HP
    @property
    def isAlive(self):
        return self.HP > 0
    @HP.setter
    def HP(self, value):
        if value < 0:
            self.__HP = 0
     #tratar de implementar mecanismos de defensa en esta función





class Character(pygame.sprite.Sprite):
    def __init__(self, win_h, win_l):

        """ The constructor of the class """
        self.ani_d = cycle((pygame.image.load(ld_img) for ld_img in glob.glob("animations/player_walk_d*")))
        self.ani_l = cycle((pygame.image.load(ld_img) for ld_img in glob.glob("animations/player_walk_l*")))
        self.ani_r = cycle((pygame.image.load(ld_img) for ld_img in glob.glob("animations/player_walk_r*")))
        self.ani_u = cycle((pygame.image.load(ld_img) for ld_img in glob.glob("animations/player_walk_u*")))
        self.win_h = win_h
        self.win_l = win_l
        self.__image = next(self.ani_d)
        self.x = win_l/2
        self.y = win_h/2
        self.distanceMoved_y = 0
        self.distanceMoved_x = 0
        self.diagonal = 0
        self.side_walking = 0

    @property
    def image(self):
        if self.distanceMoved_x %23 == 0 and self.distanceMoved_x != 0 or self.diagonal != 0:

            if self.distanceMoved_x < 0 or self.diagonal < 0:
                self.diagonal = 0
                self.distanceMoved_x = -1
                self.__image = next(self.ani_l)
                return self.__image
            if self.distanceMoved_x > 0 or self.diagonal > 0:
                self.diagonal = 0
                self.distanceMoved_x = 1
                self.__image = next(self.ani_r)
                return self.__image
        elif self.distanceMoved_y%23 == 0 and self.distanceMoved_y != 0:
            if self.distanceMoved_y < 0 or self.side_walking < 0:
                self.distanceMoved_y = -1
                self.__image = next(self.ani_u)
                return self.__image
            if self.distanceMoved_y > 0 :

                self.distanceMoved_y = 1
                self.__image = next(self.ani_d)
                return self.__image

        else:
            return self.__image

    def handle_keys(self):

        """ Handles Keys """

        key = pygame.key.get_pressed()
        vel = 1 # distance moved in 1 frame, try changing it to 5

        if key[pygame.K_LEFT] and key[pygame.K_DOWN] and key[pygame.K_RIGHT]:
            self.side_walking = 1
        if key[pygame.K_LEFT] and key[pygame.K_UP] and key[pygame.K_RIGHT]:
            self.side_walking = -1
        if key[pygame.K_DOWN] and key[pygame.K_LEFT]:
            self.diagonal = -1
        if key[pygame.K_DOWN] and key[pygame.K_RIGHT]:
            self.diagonal = 1
        if key[pygame.K_UP] and key[pygame.K_LEFT]:
            self.diagonal = -1
        if key[pygame.K_UP] and key[pygame.K_RIGHT]:
            self.diagonal = 1

        if key[pygame.K_DOWN] or key[pygame.K_UP]:
            if key[pygame.K_DOWN]:
                if self.y <= self.win_h:
                    self.distanceMoved_y += vel # down key
                    self.y += vel
                     # move dow
                else:
                    self.distanceMoved_y = 0
                    self.y = self.win_h-2
            elif key[pygame.K_UP]:
                if self.y >= 0:# up key
                    self.distanceMoved_y -= vel
                    self.y -= vel # move up
                else:
                    self.distanceMoved_y = 0
                    self.y = 2
        if key[pygame.K_LEFT] or key[pygame.K_RIGHT]:
            if key[pygame.K_RIGHT]:
                if self.x <= self.win_l: # right key
                    self.distanceMoved_x += vel
                    self.x += vel # move right
                else:

                    self.x = self.win_l-2
            elif key[pygame.K_LEFT]:
                if self.x >= 0: # left key
                    self.distanceMoved_x -= 1
                    self.x -= vel # move left
                else:
                    self.distanceMoved_x = 0
                    self.x = 2



    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))


pygame.init()
screen = pygame.display.set_mode((window_len, window_up))

PJ = Character(window_up-64, window_len-50) # create an instance
clock = pygame.time.Clock()
KEYESC = pygame.K_q
running = True

while running:
    # handle every event since the last frame.
    for event in pygame.event.get():

        if event.type == pygame.QUIT or event.type == KEYESC:
            pygame.quit() # quit the screen
            running = False

    PJ.handle_keys() # handle the keys
    screen.fill((255,255,255))
     # fill the screen with white
    PJ.draw(screen) # draw the bird to the screen
    pygame.display.update() # update the screen

    clock.tick(500)
