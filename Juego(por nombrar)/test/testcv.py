import cv2 as cv
import numpy as np
import pygame
img = cv.imread("animations/something.png")
print(img.shape)
rows,cols, bytes = img.shape
M = cv.getRotationMatrix2D((cols/2,rows/2), 0.1 ,1)
dst = cv.warpAffine(img, M , (cols,rows))
print(type(dst))
pygame.init()
screen = pygame.display.set_mode((1600, 800), pygame.RESIZABLE)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pygame.quit()
    i = 0
    clock.tick(500)
    dst = cv.warpAffine(dst, M , (cols,rows))
    obj = pygame.surfarray.make_surface(img)
    screen.fill((255,255,255))
    screen.blit(obj, (600, 300))
    screen.blit(pygame.surfarray.make_surface(dst), (0, 0))
    pygame.display.update()
    i += 1
