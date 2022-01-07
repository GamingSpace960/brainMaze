import numpy as np
import pygame as pg
import World
from time import sleep,time

class LeadBlob():
    def __init__(self,world):
        #bounds (370,310)-(450,370)
        # max spots = (450,370)/2 = (225,185)
        self.world = world
        self.restart()
        self.speed = np.random.randint(1,5)
        #self.mindSizeX = np.random.randint(5,245+1)
        #self.mindSizeY = np.random.randint(5,185+1)
        self.mindSizeX = 245
        self.mindSizeY = 185
        self.leadership = np.random.randint(1,50+1)
        self.lr = .1
        #self.qTable()

    #def qTable(self):
        #self.qtable = np.random.rand(self.mindSizeX,self.mindSizeY,4)

    def Action(self,epsilon):
        if self.dead or self.won:
            return
        if 245-(self.me.x/2) < 0 or 185-(self.me.y/2) < 0:
            print(245-(self.me.x/2),185-(self.me.y/2),self.me.x,self.me.y)
        if np.random.random() > epsilon and len(qtable) > 245-(self.me.x/2) and len(qtable[int(245-(self.me.x/2))]) > 185-(self.me.y/2):
            self.action = np.argmax(qtable[int(245-(self.me.x/2))][int(185-(self.me.y/2))])
        else:
            self.action = np.random.randint(4)

        x = int(245-(self.me.x/2))
        y = int(185-(self.me.y/2))
        
        if self.action == 0:
            self.me.move_ip(-2*self.speed,0)
        elif self.action == 1:
            self.me.move_ip(2*self.speed,0)
        elif self.action == 2:
            self.me.move_ip(0,-2*self.speed)
        else:
            self.me.move_ip(0,2*self.speed)
        score = 0
        if self.me.collidelist(self.world.walls) != -1:
            self.dead = True
            score -= 20_000
        elif self.me.colliderect(self.world.goal):
            score += 30_000-2*self.time
            self.won = True
            self.dead = True
        elif (self.me.x,self.me.y) in self.beenList:
            score -= 60
        self.beenList.append((self.me.x,self.me.y))
        score +=1
        self.score += score
        self.time+=1
        qtable[x][y][self.action] += self.lr* ((1-.99)*score + .99*max(qtable[int(245-(self.me.x/2))][int(185-(self.me.y/2))]) - qtable[x][y][self.action])

    def restart(self):
        x = np.random.randint(370/2,450/2+.5)*2
        y = np.random.randint(310/2,370/2+.5)*2
        self.me = pg.draw.rect(self.world.win,(10,10,200),(x,y,2,2))
        self.beenList = []
        self.dead = False
        self.won = False
        self.score = 0
        self.time = 0


        
