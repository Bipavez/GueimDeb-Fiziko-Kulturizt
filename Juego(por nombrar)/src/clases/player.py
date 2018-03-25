import pygame
from pygame import sprite
import glob
from itertools import cycle

window_up = 640
window_len = 1080
class Player(pygame.sprite.Sprite):
    def __init__(self,win_h  ,win_l ,img_pth = "player",speed  = 1, width = 64, height = 64):
        super(Player, self).__init__()
        self.speed = speed
        self.animation_list = {"WALK_U":[pygame.image.load(ld_img) for ld_img in glob.glob("animations/{}_walk_u*".format(img_pth))],
                         "WALK_D":[pygame.image.load(ld_img) for ld_img in glob.glob("animations/{}_walk_d*".format(img_pth))],
                         "WALK_L":[pygame.image.load(ld_img) for ld_img in glob.glob("animations/{}_walk_l*".format(img_pth))],
                         "WALK_R":[pygame.image.load(ld_img) for ld_img in glob.glob("animations/{}_walk_r*".format(img_pth))]
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

    @property
    def rect(self):
        return self.__image.get_rect()
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

        if (self.distanceMoved[1] % 23 == 0 and self.distanceMoved[1] != 0):
            if self.distanceMoved[1] < 0:
                self.distanceMoved[1] = -1
                self.__image = next(self.animations["WALK_L"])
            elif self.distanceMoved[1] > 0:
                self.distanceMoved[1] = 1
                self.__image = next(self.animations["WALK_R"])
        if (self.distanceMoved[0] % 23 == 0 and self.distanceMoved[0] != 0):
            if self.distanceMoved[0] < 0:
                self.distanceMoved[0] = -1
                self.__image = next(self.animations["WALK_U"])
            elif self.distanceMoved[0] > 0:

                self.distanceMoved[0] = 1
                self.__image = next(self.animations["WALK_D"])
        else:
            pass
        return self.__image

    def handle_keys(self):
        key = pygame.key.get_pressed()
        vel = self.speed
        if key[pygame.K_DOWN] or key[pygame.K_UP]:
            if key[pygame.K_DOWN]:
                self.going = "d"
                if self.y <= self.win_h:
                    self.distanceMoved[0] += vel # down key
                    self.y += vel
                     # move dow
                else:
                    self.distanceMoved[0] = 0
                    self.y = self.win_h-2
            if key[pygame.K_UP]:
                self.going = "u"


                if self.y >= 0:# up key
                    self.distanceMoved[0] -= vel
                    self.y -= vel # move up
                else:
                    self.distanceMoved[0] = 0
                    self.y = 2
        elif key[pygame.K_LEFT] or key[pygame.K_RIGHT]:
            if key[pygame.K_RIGHT]:
                self.going = "r"

                if self.x <= self.win_l: # right key
                    self.distanceMoved[1] += vel
                    self.x += vel # move right
                else:

                    self.x = self.win_l-2
            if key[pygame.K_LEFT]:
                self.going = "l"


                if self.x >= 0: # left key
                    self.distanceMoved[1] -= 1
                    self.x -= vel # move left
                else:
                    self.distanceMoved[1] = 0
                    self.x = 2



    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))
pygame.init()
screen = pygame.display.set_mode((window_len, window_up))

PJ = Player(window_up-64, window_len-50) # create an instance
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
