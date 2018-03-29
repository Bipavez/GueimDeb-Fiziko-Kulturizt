
import pygame
import numpy
import time
def fill_gradient(surface, color, gradient, rect=None, vertical=True, forward=True):
    """fill a surface with a gradient pattern
    Parameters:
    color -> starting color
    gradient -> final color
    rect -> area to fill; default is surface's rect
    vertical -> True=vertical; False=horizontal
    forward -> True=forward; False=reverse

    Pygame recipe: http://www.pygame.org/wiki/GradientCode
    """
    if rect is None: rect = surface.get_rect()
    x1,x2 = rect.left, rect.right
    y1,y2 = rect.top, rect.bottom
    if vertical: h = y2-y1
    else:        h = x2-x1
    if forward: a, b = color, gradient
    else:       b, a = color, gradient
    rate = (
        float(b[0]-a[0])/h,
        float(b[1]-a[1])/h,
        float(b[2]-a[2])/h
    )
    fn_line = pygame.draw.line
    if vertical:
        for line in range(y1,y2):
            color = (
                min(max(a[0]+(rate[0]*(line-y1)),0),255),
                min(max(a[1]+(rate[1]*(line-y1)),0),255),
                min(max(a[2]+(rate[2]*(line-y1)),0),255)
            )
            fn_line(surface, color, (x1,line), (x2,line))
    else:
        for col in range(x1,x2):
            color = (
                min(max(a[0]+(rate[0]*(col-x1)),0),255),
                min(max(a[1]+(rate[1]*(col-x1)),0),255),
                min(max(a[2]+(rate[2]*(col-x1)),0),255)
            )
            fn_line(surface, color, (col,y1), (col,y2))
pygame.init()
image = pygame.image.load("animations/Tree.png")
screen = pygame.display.set_mode((1600,900))
Clock = pygame.time.Clock()

array = pygame.surfarray.pixels3d(image)
class Shadow(sprite.Sprite):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.rect = self.image.get_rect()
    @property
    def image(self):
        xProy = self.rect.x + self.parent.rect.x
        dist = math.sqrt(xProy**2+(self.rect.y+self.parent.rect.y)**2)
        array = pg.surfarray.pixels3d(self.parent.image)
        rows, cols, bytes = array.shape
        M = cv.getRotationMatrix2D((rows/2+20, cols/2), 90 + math.acos(xProy/dist), 1)
        M = np.flip(M, axis=0)
        dst = cv.warpAffine(array, M, (cols+20,rows+20))
        img = pg.surfarray.make_surface(dst)
        return img
    def update(self):
        self.rect.y , self.rect.x = (self.parent.rect.y + 0.1*self.parent.rect.width*math.sin(self.parent.walk_frame*0.1),self.parent.rect.x + 0.1*self.parent.rect.width*math.sin(self.parent.walk_frame*0.1))


























class Shadow(pygame.sprite.sprite):
    def __init__(self, parent, image = None):
        self.sprite = sprite
        self.spriteArray = pygame.surfarray.pixels2d(self.sprite.image)
    @property
    def image(self):
        return self.parent.image
    def makeImage(self):
        colorkey = self.image.get_colorkey()
        transparent = colorkey if colorkey else (0,0,0,0)
        shadowStrips = list()































image = pygame.surfarray.make_surface(array)
center=(800,450)
while True:
    for event in pygame.event.get():
        key = pygame.key.get_pressed()
        if key[pygame.K_e] or key[pygame.K_TAB]:
            pygame.quit()
    array = pygame.surfarray.pixels3d(image)


    image = pygame.surfarray.make_surface(array)
 #Do the rotation
    size=image.get_size() #Store size
    hSize=[n/2 for n in size] #Half the size
    pos=(center[0]-hSize[0],center[1]-hSize[1])  #Substract half the size
#from the center
    screen.fill((0,0,0))
    screen.blit(image, pos)
    pygame.display.update()
    Clock.tick(60)
