import pygame as pg
import numpy as np
from math import *

pg.init()
size = 400, 400

screen = pg.display.set_mode(size, pg.HWSURFACE)

imagen = pg.image.load("animations/ball_1.png")
imagen = imagen.convert_alpha()
screen.fill((255,255,0))
screen.blit(imagen, (0,0))
while True:
    for event in pg.event.get():
        print(event)
        if pg.key.get_pressed()[pg.K_SPACE]:
            pg.quit() # quit the screen
            running = False
        if event.type == pg.QUIT:
                pg.quit() # quit the screen
                running = False
        if pg.key.get_pressed()[pg.K_f]:
            if "1920" in str(pg.display.Info()):
                window_up = 900
                window_len = 1600
                screen = pg.transform.scale(screen, (window_len, window_up))
            else:
                window_up = 1080
                window_len = 1920
                screen = pg.transform.scale(screen, (window_len, window_up), FULLSCREEN)

    alpha = imagen.get_alpha()
    print(alpha)
    imagen.set_alpha(alpha//2)

    screen.fill((0,255,0))
    screen.blit(imagen, (0,0))

    pg.time.delay(100)
    pg.display.update()




"""
import numpy as np

class Network:
    def __init___(self,sizes):  #Lista con cantidades de neuronas por capa
        self.num_layers=len(sizes)
        self.sizes=sizes
        self.biases=[np.random.randn(y,1) for y in sizes[1:]]   #randn crea un vector de largo y
        self.weights=[np.random.randn(y,x) for x,y in zip(sizes[:-1],sizes[1:])] #Crea para cada capa una matriz de pesos

    def feedforward(self,a):    #a es input, devuelcve output final
        for b,w in zip(self.biases,self.weights):
            a=sigmoid(np.dot(w,a)+b)    #Dot es producto matricial, sigmoid actúa vectorialmente
        return a    #Cada iteración da los resultados de cada capa. Devuelve final

    def SGD(self,training_data,epochs,mini_batch_size,eta,test_data=None):
        if test_data is not None: n_test=len(test_data)
        n=len(training_data)
        for j in xrange(epochs):
            random.shuffle(traninig_data)
            mini_batches=[training_data[k:k+mini_batch_size]
                          for k in xrange(0,n,mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch,eta)
            if test_data:
                print("Epoch {}: {}/{}".format(j,self.evaluate(test_data),n_test))
            else:
                print("Epoch {} complete".format(j))

    def update_mini_batch(self,mini_batch,eta):
        nabla_b=[np.zeroes(b.shape) for b in self.biases]
        nabla_w=[np.zeroes(w.shape) for w in self.weights]
        for x,y in mini_batch:
            delta_nabla_b,delta_nabla_w = self.backdrop(x,y)
            nabla_b=[nb+dnb for nb,dnb in zip(nabla_b,delta_nabla_b)]
            nabla_w=[nw+dnw for nw,dnw in zip(nabla_w,delta_nabla_w)]
        self.weights = [w-nw*eta/len(mini_batch) for w,nw in zip(self.weights,nabla_w)]
        self.biases = [b-nb*eta/len(mini_batch) for b,nb in zip(self.biases,nabla_b)]

def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))

def sigmoid_prime(z):
    return sigmoid(z)*(1-sigmoid(z))
    """
