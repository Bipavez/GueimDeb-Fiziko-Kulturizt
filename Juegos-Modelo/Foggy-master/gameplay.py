from random import randint, choice

import pygame as pg
import pygame.gfxdraw as gfxdraw

from prepare import GFX, SCREEN_RECT
from state_engine import GameState
from player import Player
from wolf import Wolf
from shadow import Shadow


def footprint_collide(sprite1, sprite2):
    return sprite1.footprint.colliderect(sprite2.footprint)


def make_background(size, tile_size=64):
    grass = GFX["grass"]
    w, h  = size
    surf = pg.Surface(size).convert()
    for y in range(0, h + 1, tile_size):
        for x in range(0, w + 1, tile_size):
            surf.blit(grass, (x, y))
    return surf
    

class Tree(pg.sprite.Sprite):
    def __init__(self, pos, *groups):
        super(Tree, self).__init__(*groups)
        self.trunk = choice(("curvy", "straight"))
        self.image = GFX["{}-tree{}".format(self.trunk, randint(1, 4))]
        self.rect = self.image.get_rect(midbottom=pos)
        x, y = self.rect.topleft
        if self.trunk == "curvy":
            self.footprint = pg.Rect(x + 65, y + 102, 16, 11)
        else:
            self.footprint = pg.Rect(x + 39, y + 102, 14, 10)


class Gameplay(GameState):
    def __init__(self):
        super(Gameplay, self).__init__()
        w, h = SCREEN_RECT.size
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.background = make_background((w, h))
        self.fog = pg.Surface((w, h), pg.SRCALPHA)
        self.fog.fill((0, 0, 0, 255))
        self.player = Player(SCREEN_RECT.center, self.all_sprites)
        self.wolves = pg.sprite.Group()
        for _ in range(10):
            pos = randint(32, w - 32), randint(32, h - 32)
            Wolf(pos, self.wolves, self.all_sprites)
        self.trees = pg.sprite.Group()
        for _ in range(25):
            pos = randint(0, w), randint(0, h)
            Tree(pos, self.trees, self.all_sprites)

        self.tree_shadows = []
        for tree in self.trees:
            self.tree_shadows.append(Shadow(tree.footprint))
        
    def startup(self, persistent):
        self.persist = persistent

    def get_event(self,event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        self.player.get_event(event)

    def render_fog(self):

        self.fog.fill((0, 0, 0, 255))
        # self.fog.blit(self.player.seen, (0, 0))
        m = 255/float(200)
        for i in range(200, 1, -1):
            pg.draw.circle(self.fog, (0, 0, 0, i*m), self.player.get_int_pos(), i)
        
    def update(self, dt):
        self.player.update(dt)
        self.wolves.update(dt)
        player_hits = pg.sprite.spritecollide(self.player, self.trees,
                    False, collided=footprint_collide)
        for tree in player_hits:
            self.player.collide(tree)
        wolf_hits = pg.sprite.groupcollide(self.wolves, self.trees,
                    False, False, collided=footprint_collide)
        for wolf in wolf_hits:
            for tree in wolf_hits[wolf]:
                x, y = wolf.footprint.topleft
                w, h = wolf.footprint.size
                moves = {
                        (-1, 0): (tree.footprint.right, y),
                        (1, 0): (tree.footprint.left - w, y),
                        (0, -1): (x, tree.footprint.bottom),
                        (0, 1): (x, tree.footprint.top - h)}
                wolf.footprint.topleft = moves[wolf.direction]
                dx, dy = wolf.footprint.x - x, wolf.footprint.y - y
                wolf.rect.move_ip(dx, dy)
        for sprite in self.all_sprites:
            self.all_sprites.change_layer(sprite, sprite.footprint.bottom)

        for shadow in self.tree_shadows:
            shadow.update(self.player.footprint.center)
        
    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        for shadow in self.tree_shadows:
            shadow.draw(surface)
        self.all_sprites.draw(surface)
        self.render_fog()
        surface.blit(self.fog, (0, 0))
