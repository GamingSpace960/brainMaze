import numpy as np
import pygame as pg
import World
from time import sleep

class LeadBlob():
    def __init__(self,world):
        #bounds (370,310)-(450,370)
        # max spots = (450,370)/2 = (225,185)
        self.world = world
        self.restart()
        self.speed = np.random.randint(1,5)
        self.mindSizeX = np.random.randint(5,250+1)
        self.mindSizeY = np.random.randint(5,185+1)
        self.leadership = np.random.randint(1,50+1)
        self.qTable()

    def qTable(self):
        self.qtable = np.random.randn(self.mindSizeX,self.mindSizeY,4)

    def Action(self,epsilon):
        if self.dead:
            return
        if 250-(self.me.x/2) < 0 or 185-(self.me.y/2) < 0:
            print(250-(self.me.x/2),185-(self.me.y/2),self.me.x,self.me.y)
        if np.random.random() > epsilon and len(self.qtable) > 250-(self.me.x/2) and len(self.qtable[int(250-(self.me.x/2))]) > 185-(self.me.y/2):
            self.action = np.argmax(self.qtable[int(250-(self.me.x/2))][int(185-(self.me.y/2))])
        else:
            self.action = np.random.randint(4)
        if self.action == 0:
            self.me.move_ip(-2*self.speed,0)
        elif self.action == 1:
            self.me.move_ip(2*self.speed,0)
        elif self.action == 2:
            self.me.move_ip(0,-2*self.speed)
        else:
            self.me.move_ip(0,2*self.speed)
        if self.me.collidelist(self.world.walls) != -1:
            self.dead = True
            self.score -= 1000
            return
        elif self.me.colliderect(self.world.goal):
            self.score += 100
        elif (self.me.x,self.me.y) in self.beenList:
            self.score -= 10
        else:
            self.score -=.1
        pg.draw.rect(self.world.win,(10,10,200),self.me)
    def restart(self):
        x = np.random.randint(370/2,450/2+.5)*2
        y = np.random.randint(310/2,370/2+.5)*2
        self.me = pg.draw.rect(self.world.win,(10,10,200),(x,y,2,2))
        self.beenList = []
        self.dead = False
        self.score = 0


        
world = World.World()
bobs = [LeadBlob(world) for _ in range(10_000)]

epsilon = 1
epsilonDecay = .001
step = 0
while True:
    while step < 10_000 and False in [bob.dead for bob in bobs]:
        world.draw()
        for bob in bobs:
            bob.Action(epsilon)
        world.update()
        step+= 1
        
    for bob in bobs:
            bob.restart()
    epsilon -= epsilon*epsilonDecay
    print(epsilon)
    step = 0
    done = False