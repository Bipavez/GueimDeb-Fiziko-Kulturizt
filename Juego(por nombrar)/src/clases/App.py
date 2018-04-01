import pygame as pg
from pygame import sprite
from pygame.locals import *
import time
import math

from Control import *       #En algún momento poner referencias
from Sprites import *
from ImageProcessing import *
from settings import *
from ambiente import *
"""
Este módulo es para que hagamos la clase App,
por hoy estpa de forma muy primitiva, hay que hacerla de nuevo
"""
def initTest(App, W, H, FOG):
    App.player = Character_Sprite("player", 5)

    App.p_l, App.p_h = App.player.rect.width, App.player.rect.height
    App.player.x, App.player.y = W//2 - App.p_l//2, H//2 - App.p_h//2 #Cambiar, limpiar
    App.FOG = FOG
    App.fog = draw_fog(App.size, App.FOG)
    App.ball = Item_Sprite("ball", App.player)
    App.npc = Character_Sprite("player",0)
    App.npc.x, App.npc.y = 400,300
    App.player_alone = sprite.Group(App.player)
    App.player_entities = sprite.Group(App.player, App.ball)
    App.fire = fuenteLuz("fire/",300, App.player_alone)
    App.background_entities = sprite.Group(App.npc)
    App.light_entities = sprite.Group(App.fire)
    App.collision_entities = sprite.Group(App.player, App.npc)
    App.CAMERA_X = App.player.x - W//2 + App.p_l//2
    App.CAMERA_Y = App.player.y - H//2 + App.p_h//2
    pg.mixer.music.load("music/theme2.mid")
    pg.mixer.music.play()
def events():
	for event in pg.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			pg.quit()
			sys.exit()

class App:
    def __init__(self, size, backgroundPath, sprites):
        self.width, self.height = size
        self.screen = None
        self.background = None
        self.sprites = sprites
        self.size = size
        self.backgroundPath = backgroundPath
        self.clock = pg.time.Clock()
        self.fps = self.clock.get_fps()
        self.initialized = False
    def initPg(self):
        pg.init()
        pg.font.init()
        self.font = pg.font.SysFont("Comic Sans MS", 30)
        self.text = self.font.render(str(self.clock.get_fps()), False, (0,0,0))
        self.screen = pg.display.set_mode(self.size)
        self.background = pg.image.load(self.backgroundPath)
    def mainLoop(self):
        if not self.initialized:
            self.initPg()
            initTest(self, self.width, self.height, 0)
            self.initialized = True

            #Screen filling
        self.Points = False
        self.text = self.font.render(str(round(self.clock.get_fps())), False, (255,255,255))
        self.screen.fill((0,0,0))
        self.screen.blit(self.background, (-self.CAMERA_X,-self.CAMERA_Y, self.width, self.height))
        self.screen.blit(self.text, (0,0))
        keys = pg.key.get_pressed()
        if keys[pg.K_p]:
            if self.Points is True:
                self.Points = False
            elif self.Points is False:

                self.Points = True
        if self.Points:

            pg.draw.circle(self.screen, (255,255,255), (self.player.rect.centerx, self.player.rect.centery), 5)
            pg.draw.circle(self.screen, (255,255,0), (self.fire.rect.centerx, self.fire.rect.centery), self.fire.radius)
        self.player_entities.draw(self.screen)
        self.background_entities.draw(self.screen)
        self.light_entities.draw(self.screen)
        if self.FOG != 0:
            self.screen.blit(self.fog, (0,0))
        ##



        #Event handling
        handle_keys(self.player)
        events()
        if self.Points:
            pg.draw.line(self.screen, (255,255,255),
                         [self.player.rect.centerx+self.player.corrections[0], self.player.rect.centery+self.player.corrections[1]],
                         [self.fire.rect.centerx, self.fire.rect.centery], 5)

        ##

        self.player_entities.update(self.CAMERA_X, self.CAMERA_Y)
        self.background_entities.update(self.CAMERA_X, self.CAMERA_Y)
        self.light_entities.update(self.CAMERA_X, self.CAMERA_Y)

        self.clock.tick(60)
        pg.display.set_caption("{}".format(self.clock.get_fps()))

        self.CAMERA_X = self.player.x - self.width//2 + self.p_l//2
        self.CAMERA_Y = self.player.y - self.height//2 + self.p_h//2
        pg.display.update()
