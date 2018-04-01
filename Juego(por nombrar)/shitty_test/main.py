import pygame
from pygame.locals import *
from numpy import *
import math
import cv2
import glob
import os

pygame.init()

window_len = 960
window_up = 640

fps = 30

screen = pygame.display.set_mode((window_len, window_up), RESIZABLE)

pygame.mixer.music.load("music/theme2.mid")
pygame.mixer.music.play()

pygame.display.set_caption("Juego")

clock = pygame.time.Clock()


def rotate_image(rotation_matrix, rotation_angle):
    # Rotates an image (rotation_angle in degrees) and expands image to avoid cropping
    height, width, image_bytes = rotation_matrix.shape
    image_center = (width / 2, height / 2)
    # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape

    rotation_mat = cv2.getRotationMatrix2D(image_center, 90 + rotation_angle, 1.0)

    # rotation calculates the cos and sin, taking absolutes of those.
    abs_cos = abs(rotation_mat[0, 0])
    abs_sin = abs(rotation_mat[0, 1])

    # find the new width and height bounds
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    # subtract old image center (bringing image back to origo) and adding the new image center coordinates
    rotation_mat[0, 2] += bound_w / 2 - image_center[0]
    rotation_mat[1, 2] += bound_h / 2 - image_center[1]

    # rotate image with the new bounds and translated rotation matrix
    rotated_mat = cv2.warpAffine(rotation_matrix, rotation_mat, (bound_w, bound_h))

    return rotated_mat


class Shadow(pygame.sprite.Sprite):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        try:
            self.rect = self.image.get_rect()
        except:
            self.rect = self.parent.image.get_rect()

    @property
    def array(self):
        return pygame.surfarray.pixels3d(
            self.parent.image if self.rect.y < self.parent.rect.y else pygame.transform.flip(self.parent.image, True,
                                                                                             False))

    @property
    def image(self):
        v_1 = array((1, 0))
        vectorector_2 = array((self.rect.x - self.parent.rect.centerx + 25,
                               self.rect.y - self.parent.rect.y + self.rect.centery - self.parent.rect.centery))
        v_2 = vectorector_2 / linalg.norm(vectorector_2)
        draw_angle = math.acos(dot(v_2, v_1)) if self.rect.y > self.parent.rect.y else -math.acos(dot(v_2, v_1))
        dst = rotate_image(self.array, degrees([draw_angle]))
        im_gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        (thresh, im_bw) = cv2.threshold(im_gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_TRIANGLE)
        kernel = ones((3, 3), uint8)
        im_bw = cv2.erode(im_bw, kernel, iterations=1)
        shading = [pygame.surfarray.make_surface(cv2.dilate(im_bw, kernel, iterations=i * 2)) for i in range(12)]
        for i, shade in enumerate(shading):
            shade.set_alpha(i * 15 + 200)
        surf = pygame.surfarray.make_surface(im_bw)
        surf.set_alpha(75)
        # im_bw = cv2.morphologyEx(im_bw, cv2.MORPH_GRADIENT, kernel)
        img = surf.convert()
        img.set_colorkey((255, 255, 255))
        return img

    def update(self, camera_pos_x, camera_pos_y):
        x_final = self.parent.position[0] - camera_pos_x - 5
        y_final = self.parent.rect.bottom + 2 * self.parent.position[2] - 7
        self.rect.x, self.rect.y = x_final, y_final


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
              Character('Otra persona', 'player', 10, 10, 10, 10, 10, 10)]

characters_ids = []
for character in characters:
    characters_ids.append(character.sprite)

# Todos los personajes que no salgan ahí arriba serán NPC de relleno (o no pelean)


class Player(pygame.sprite.Sprite):
    # Estoy de acuerdo con que esta clase sea general y que sirva tanto para generar a los
    # personajes jugables como a los NPC. Propongo que se llame Player para abreviar.
    # identifier cumple la función que antes tenía img_pth: sirve para asignar sprites
    # solo que ahora, si al personaje le ponemos un identifier que SÍ aparece en characters,
    # entonces adquirirá sus características (stats base) acorde al nivel.
    def __init__(self, identifier, abscissa, ordinate, dimension, width=64, height=64, depth=64, leader=False, level=1):
        super().__init__()
        if os.path.exists('images/' + str(identifier)):
            self.sprite = identifier
        else:
            self.sprite = 'player'
        self.position = array((abscissa, ordinate, dimension))
        # Agregué una coordenada z para facilitar la creación de mapas con relieve.
        self.animation_list = {
            "WALK_U": [pygame.image.load(i).convert() for i in glob.glob('images\\{}\\walk_u*'.format(self.sprite))],
            "WALK_D": [pygame.image.load(i).convert() for i in glob.glob('images\\{}\\walk_d*'.format(self.sprite))],
            "WALK_L": [pygame.image.load(i).convert() for i in glob.glob('images\\{}\\walk_l*'.format(self.sprite))],
            "WALK_R": [pygame.image.load(i).convert() for i in glob.glob('images\\{}\\walk_r*'.format(self.sprite))]}
        for i in self.animation_list:  # Hace el blanco transparente.
            for animation_key in self.animation_list[i]:
                pygame.PixelArray(animation_key).replace((255, 255, 255), (0, 0, 0))
                animation_key.set_colorkey((0, 0, 0))
        self.width = width
        self.height = height
        self.depth = depth
        self.speed = 6
        self.derivatives = 0
        # Cantidad de derivadas distintas de cero que tiene el vector posición. Si es 0, está en absoluto reposo.
        # Si es 1, se mueve con velocidad constante. Si es 2, de seguro está saltando.
        self.velocity = array((0.0, 0.0, 0.0))  # ES EL VECTORECTOR VELOCIDAD. Si es [0, 0, 0], está en reposo.
        self.acceleration = array((0.0, 0.0, 0.0))
        self.walking = 0  # Contador de pasos. Creo que en el archivo player.py tenía otro nombre.
        self.direction = array((1.0, 0.0))  # Vectorector unitario que indica hacia dónde mira el personaje.
        if identifier in characters_ids:
            self.level = level
        else:
            self.level = 1
        self.hp = 1  # Después inventamos una fórmula para calcular el HP conforme al nivel.
        self.max_hp = 1  # Ídem
        self.sp = 1  # Same here
        self.max_sp = 1  # ...and here
        self.rect = self.image.get_rect()
        self.leader = leader  # No sé si esto servirá de algo algún día. Lo pongo por si acaso.

    def update(self, camera_pos_x, camera_pos_y):
        self.rect.x, self.rect.y = self.position[0] - camera_pos_x, self.position[1] - self.position[2] - camera_pos_y

    @property
    def image(self):
        # Añadí este método para que no sea necesario el atributo __image.
        # Lo que hace es calcular automáticamente el frame que toca al caminar
        # y lo dibuja. Supongo que de esta forma es más simple.
        # También el uso del cycle se hace innecesario.
        animation_speed = fps / 5
        if self.walking + 1 >= len(self.animation_list['WALK_U']) * animation_speed:
            self.walking = 0
        if self.derivatives > 0:
            frame = round(self.walking // animation_speed)
            self.walking += 1
        else:
            frame = 1
        image_frame = self.animation_list['WALK_U'][frame]
        if array_equal(self.direction, array((0, -1))):  # La dirección (0, -1) es up.
            image_frame = self.animation_list['WALK_U'][frame]
        elif array_equal(self.direction, array((0, 1))):
            image_frame = self.animation_list['WALK_D'][frame]
        elif array_equal(self.direction, array((-1, 0))):  # La dirección (-1, 0) es left.
            image_frame = self.animation_list['WALK_L'][frame]
        elif array_equal(self.direction, array((1, 0))):
            image_frame = self.animation_list['WALK_R'][frame]
        # Ahora, veamos los sprites diagonales.
        elif self.direction[0] > 0:
            if self.direction[1] > 0:
                image_frame = self.animation_list['WALK_R'][frame]
            elif self.direction[1] < 0:
                image_frame = self.animation_list['WALK_R'][frame]
        elif self.direction[0] < 0:
            if self.direction[1] > 0:
                image_frame = self.animation_list['WALK_L'][frame]
            elif self.direction[1] < 0:
                image_frame = self.animation_list['WALK_L'][frame]
        return image_frame


class Equipment(pygame.sprite.Sprite):
    def __init__(self, img_pth, parent):
        super().__init__()
        self.animation_list = {
            "BALL_MOVE": [pygame.image.load(i) for i in glob.glob("images/items/{}_**".format(img_pth))]}
        self.parent = parent
        self.__animation_count = 0
        self.position = parent.position + array((-20, 0, 25))
        self.rect = self.image.get_rect()

    @property
    def image(self):
        animation_speed = fps / 2
        if self.__animation_count + 1 >= len(self.animation_list['BALL_MOVE']) * animation_speed:
            self.__animation_count = 0
        frame = round(self.__animation_count // animation_speed)
        self.__animation_count += 1
        return self.animation_list['BALL_MOVE'][frame]

    def update(self, camera_pos_x, camera_pos_y):
        self.position = self.parent.position + array((-20, 0, 64))
        self.rect.x = self.position[0] - camera_pos_x
        self.rect.y = self.position[1] - self.position[2] - camera_pos_y


# A poner niebla se ha dicho.

def draw_fog(circle_size, depth):
    fog_style = pygame.Surface(circle_size, pygame.SRCALPHA)
    fog_style.fill((0, 0, 0, 255))
    for i in range(255, 1, -1):
        pygame.draw.circle(fog_style, (0, 0, 0, i), (circle_size[0] // 2, circle_size[1] // 2), round(i * depth))
    return fog_style


def normalize(vector):
    norm = linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm

fog_mode = 0
fog = ''
if fog_mode != 0:
    fog = draw_fog((window_len, window_up), fog_mode)

background = pygame.image.load("images\\background.png")
player = Player('medi', 10, 10, 0, 40, 64, 64, True)
player.position[0] = window_len // 2 - player.width // 2
player.position[1] = window_up // 2 - player.height // 2
ball = Equipment('ball', player)
npctest = Player('medi', 50, 69, 0, 40, 50, 64, True)
player_entities = pygame.sprite.Group(player, ball)
background_entities = pygame.sprite.Group(npctest)
shadow_entities = pygame.sprite.Group(Shadow(player), Shadow(ball))
for id_npc in background_entities:
    shadow_entities.add(Shadow(id_npc))
camera_x = player.position[0] - window_len // 2 + player.width // 2
camera_y = player.position[1] - window_up // 2 + player.height // 2
points = False
keep_jumping = False
running = True
while running:
    clock.tick(fps)
    screen.fill((0, 0, 0))
    screen.blit(background, (-camera_x, -camera_y, window_len, window_up))
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_SPACE] or event.type == pygame.K_q:
            running = False
    if player.derivatives == 1:
        player.direction = normalize(player.velocity[:2])
        player.velocity = array((0.0, 0.0, 0.0))
    if 1 in keys:
        if keys[pygame.K_UP]:
            player.velocity += array((0.0, -1.0, 0.0))
        if keys[pygame.K_DOWN]:
            player.velocity += array((0.0, 1.0, 0.0))
        if keys[pygame.K_LEFT]:
            player.velocity += array((-1.0, 0.0, 0.0))
        if keys[pygame.K_RIGHT]:
            player.velocity += array((1.0, 0.0, 0.0))
        if player.derivatives == 0 and not array_equal(player.velocity, array((0.0, 0.0, 0.0))):
            player.derivatives = 1
        if keys[pygame.K_z]:
            if keep_jumping:
                if player.derivatives == 1 and array_equal(player.velocity, array((0.0, 0.0, 0.0))):
                    player.derivatives = 0
            else:
                keep_jumping = True
                if player.acceleration[2] == 0:
                    player.velocity[2] = 25.0
                    player.position[2] = 0.01

        if pygame.key.get_pressed()[pygame.K_f]:
            if "960" in str(pygame.display.Info()):
                window_up = 320
                window_len = 480
                screen = pygame.transform.scale(screen, (window_len, window_up))
                pygame.display.set_mode((window_len, window_up), RESIZABLE)
            else:
                window_up = 640
                window_len = 960
                screen = pygame.transform.scale(screen, (window_len, window_up))
                pygame.display.set_mode((window_len, window_up), RESIZABLE)
            camera_x = player.position[0] - window_len // 2 + player.width // 2
            camera_y = player.position[1] - window_up // 2 + player.height // 2
            screen.blit(background, (-camera_x, -camera_y, window_len, window_up))
    elif player.derivatives > 0:
        player.derivatives = 0
    if keep_jumping and not keys[pygame.K_z]:
        keep_jumping = False
    if player.position[2] != 0:
        # Cambiar después. En estricto rigor, la condición es:
        # "si el jugador está parado sobre un tileset penetrable", entonces adquirirá la aceleración de graverdad,
        # pero como aún no creamos los tilesets, no lo puse así.
        player.acceleration = array((0.0, 0.0, -5.0))
        player.derivatives = 2
    if player.derivatives > 0:
        player.velocity += player.acceleration
        player.direction = normalize(player.velocity[:2])
        player.velocity[0] = player.direction[0] * player.speed
        player.velocity[1] = player.direction[1] * player.speed
        final_position = player.position + player.velocity
        if player.derivatives == 2 and final_position[2] <= 0:  # Cuando el jugador llegue al piso, dejará de caer.
            final_position[2] = 0
            player.acceleration[2] = 0
            player.velocity[2] = 0
            player.derivatives -= 1
            if player.derivatives < 0:
                player.derivatives = 0
        collision = False
        for id_npc in background_entities:
            pos1 = final_position
            pos2 = id_npc.position
            if 0 <= pos1[0] - pos2[0] <= id_npc.width:
                if 0 <= pos1[1] - pos2[1] <= id_npc.height:
                    if 0 <= pos1[2] - pos2[2] <= id_npc.depth:
                        collision = True
                        break
                    if 0 <= pos1[2] - pos2[2] + player.depth <= id_npc.depth:
                        collision = True
                        break
                if 0 <= pos1[1] - pos2[1] + player.height <= id_npc.height:
                    if 0 <= pos1[2] - pos2[2] <= id_npc.depth:
                        collision = True
                        break
                    if 0 <= pos1[2] - pos2[2] + player.depth <= id_npc.depth:
                        collision = True
                        break
            if 0 <= pos1[0] - pos2[0] + player.width <= id_npc.width:
                if 0 <= pos1[1] - pos2[1] <= id_npc.height:
                    if 0 <= pos1[2] - pos2[2] <= id_npc.depth:
                        collision = True
                        break
                    if 0 <= pos1[2] - pos2[2] + player.depth <= id_npc.depth:
                        collision = True
                        break
                if 0 <= pos1[1] - pos2[1] + player.height <= id_npc.height:
                    if 0 <= pos1[2] - pos2[2] < id_npc.depth:
                        collision = True
                        break
                    if 0 <= pos1[2] - pos2[2] + player.depth <= id_npc.depth:
                        collision = True
                        break

        if window_len - player.height > final_position[0] > 0 and window_up - player.width > final_position[1] > 0\
                and not collision:
            player.position = final_position
    background_entities.draw(screen)
    background_entities.update(camera_x, camera_y)
    player_entities.draw(screen)
    player_entities.update(camera_x, camera_y)
    shadow_entities.draw(screen)
    shadow_entities.update(camera_x, camera_y)
    if fog_mode != 0:
        screen.blit(fog, (0, 0))

    if keys[pygame.K_p]:
        if points is True:
            points = False
        elif points is False:
            points = True
    if points:
        pygame.draw.circle(screen, (255, 255, 255), (player.rect.centerx, player.rect.centery), 5)
    pygame.display.set_caption('Juego (FPS: ' + str(clock.get_fps()) + ')')
    camera_x = player.position[0] - window_len // 2 + player.width // 2
    camera_y = player.position[1] - window_up // 2 + player.height // 2
    pygame.display.update()

pygame.quit()
