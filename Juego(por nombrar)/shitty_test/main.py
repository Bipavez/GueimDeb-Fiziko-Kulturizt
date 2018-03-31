import pygame
from pygame.locals import *
from numpy import *
import glob
import os

# Este archivo de prueba usa NUUUUUMPYYYYY indicar la posición vectorial del jugador. No está actualizado
# a todas las cosas que pusieron a testear eso sí. En realidad, este archivo es más que nada para probar
# las músicas.

pygame.init()

window_len = 960
window_up = 640

fps = 60

screen = pygame.display.set_mode((window_len, window_up), RESIZABLE | FULLSCREEN)

pygame.mixer.music.load("music/theme2.mid")
pygame.mixer.music.play()

pygame.display.set_caption("Juego")

clock = pygame.time.Clock()


class Character:
    def __init__(self, nickname, sprite, hp, sp, attack, defense, special_attack, speed):
        self.name = nickname
        self.sprite = sprite
        self.hp = hp  # HP base. Usaremos alguna fórmula rebuscada para calcularlo en base a su nivel.
        self.sp = sp  # SP base. Los ataques mágicos gastan estos puntos (son típicos)
        self.attack = attack  # Ataque base al usar algún movimiento que no sea mágico (ejemplo, un puñetazo)
        self.defense = defense  # Defensa base. Algún día inventaremos fórmulas para calcular daño.
        self.special_attack = special_attack  # El ataque que usa un movimiento mágico.
        self.speed = speed  # Velocidad, pero no para moverse en el mapa, sino en batalla.

characters = [Character('Medi', 'medi', 10, 10, 10, 10, 10, 10),
              Character('Lily', 'lily', 10, 10, 10, 10, 10, 10),
              Character('Jumper', 'jumper', 10, 10, 10, 10, 10, 10),
              Character('Rob', 'rob', 10, 10, 10, 10, 10, 10)]

characters_ids = []
for character in characters:
    characters_ids.append(character.sprite)

# Todos los personajes que no salgan ahí arriba serán NPC de relleno (o no pelean)


class Player(object):
    # Estoy de acuerdo con que esta clase sea general y que sirva tanto para generar a los
    # personajes jugables como a los NPC. Propongo que se llame Player para abreviar.
    # identifier cumple la función que antes tenía img_pth: sirve para asignar sprites
    # solo que ahora, si al personaje le ponemos un identifier que SÍ aparece en characters,
    # entonces adquirirá sus características (stats base) acorde al nivel.
    def __init__(self, identifier, abscissa, ordinate, dimension, width=64, height=64, depth=64, leader=False, level=1):
        if os.path.exists('images/' + str(identifier)):
            self.sprite = identifier
        else:
            self.sprite = 'player'
        self.position = array((abscissa, ordinate, dimension))
        # Agregué una coordenada z para facilitar la creación de mapas con relieve.
        self.animation_list = {
            "WALK_U": [pygame.image.load(i) for i in glob.glob('images/{}/walk_u*'.format(self.sprite))],
            "WALK_D": [pygame.image.load(i) for i in glob.glob('images/{}/walk_d*'.format(self.sprite))],
            "WALK_L": [pygame.image.load(i) for i in glob.glob('images/{}/walk_l*'.format(self.sprite))],
            "WALK_R": [pygame.image.load(i) for i in glob.glob('images/{}/walk_r*'.format(self.sprite))]}
        self.width = width
        self.height = height
        self.depth = depth
        self.speed = 4
        self.velocity = array((0.0, 0.0, 0.0))  # ES EL VECTORECTOR VELOCIDAD. Si es [0, 0, 0], está en reposo.
        self.walking = 0  # Contador de pasos. Creo que en el archivo player.py tenía otro nombre.
        self.direction = array((1, 0))  # Vectorector unitario que indica hacia dónde mira el personaje.
        if identifier in characters_ids:
            self.level = level
        else:
            self.level = 1
        self.hp = 1  # Después inventamos una fórmula para calcular el HP conforme al nivel.
        self.max_hp = 1  # Ídem
        self.sp = 1  # Same here
        self.max_sp = 1  # ...and here
        self.leader = leader  # No sé si esto servirá de algo algún día. Lo pongo por si acaso.

    def draw(self):
        # Añadí este método para que no sea necesario el atributo __image.
        # Lo que hace es calcular automáticamente el frame que toca al caminar
        # y lo dibuja. Supongo que de esta forma es más simple.
        # También el uso del cycle se hace innecesario.
        animation_speed = fps / 20
        if self.walking + 1 >= len(self.animation_list['WALK_U']) * animation_speed:
            self.walking = 0
        if not array_equal(self.velocity, array((0, 0, 0))):
            frame = round(self.walking // animation_speed)
            self.walking += 1
        else:
            frame = 1
        if array_equal(self.direction, array((0, -1))):  # La dirección (0, -1) es up.
            screen.blit(self.animation_list['WALK_U'][frame], self.position[:2])
        elif array_equal(self.direction, array((0, 1))):
            screen.blit(self.animation_list['WALK_D'][frame], self.position[:2])
        elif array_equal(self.direction, array((-1, 0))):  # La dirección (-1, 0) es left.
            screen.blit(self.animation_list['WALK_L'][frame], self.position[:2])
        elif array_equal(self.direction, array((1, 0))):
            screen.blit(self.animation_list['WALK_R'][frame], self.position[:2])
        # Ahora, veamos los sprites diagonales.
        elif self.direction[0] > 0 and self.direction[1] > 0:
            screen.blit(self.animation_list['WALK_R'][frame], self.position[:2])
        elif self.direction[0] < 0 and self.direction[1] > 0:
            screen.blit(self.animation_list['WALK_L'][frame], self.position[:2])
        elif self.direction[0] < 0 and self.direction[1] < 0:
            screen.blit(self.animation_list['WALK_L'][frame], self.position[:2])
        elif self.direction[0] > 0 and self.direction[1] < 0:
            screen.blit(self.animation_list['WALK_R'][frame], self.position[:2])


class Equipment(pygame.sprite.Sprite):
    def __init__(self, img_pth, parent):
        super().__init__()
        self.animation_list = {
            "BALL_MOVE": [pygame.image.load(i) for i in glob.glob("images/items/{}_**".format(img_pth))]}
        self.parent = parent
        self.__animation_count = 0

    def draw(self):
        animation_speed = fps / 2
        if self.__animation_count + 1 >= len(self.animation_list['BALL_MOVE']) * animation_speed:
            self.__animation_count = 0
        frame = round(self.__animation_count // animation_speed)
        self.__animation_count += 1
        item_x = self.parent.position[0]
        item_y = self.parent.position[1]
        screen.blit(self.animation_list['BALL_MOVE'][frame], (item_x - 20, item_y - 20))


def normalize(vector):
    norm = linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm

player = Player('medi', 10, 10, 0, 64, 64, 64, True)
ball = Equipment('ball', player)
running = True
while running:
    clock.tick(fps)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_SPACE] or event.type == pygame.K_q:
            running = False
    if not array_equal(player.velocity, array((0.0, 0.0, 0.0))):
        player.direction = normalize(player.velocity[:2])
    player.velocity = array((0.0, 0.0, 0.0))
    if 1 in keys:
        if keys[pygame.K_UP]:
            player.velocity += array((0.0, -player.speed, 0.0))
        if keys[pygame.K_DOWN]:
            player.velocity += array((0.0, player.speed, 0.0))
        if keys[pygame.K_LEFT]:
            player.velocity += array((-player.speed, 0.0, 0.0))
        if keys[pygame.K_RIGHT]:
            player.velocity += array((player.speed, 0.0, 0.0))
        if not array_equal(player.velocity, array((0.0, 0.0, 0.0))):
            player.direction = normalize(player.velocity[:2])
        player.velocity = normalize(player.velocity) * player.speed
        new_position = player.position + player.velocity
        if window_len - player.height > new_position[0] > 0 and window_up - player.width > new_position[1] > 0:
            player.position = new_position

        if pygame.key.get_pressed()[pygame.K_f]:
            if "960" in str(pygame.display.Info()):
                window_up = 480
                window_len = 320
                screen = pygame.transform.scale(screen, (window_len, window_up))
                pygame.display.set_mode((window_len, window_up), RESIZABLE)
            else:
                window_up = 960
                window_len = 640
                screen = pygame.transform.scale(screen, (window_len, window_up))
                pygame.display.set_mode((window_len, window_up), RESIZABLE | FULLSCREEN)
    screen.fill((0, 0, 0))
    player.draw()
    ball.draw()
    pygame.display.update()

pygame.quit()
