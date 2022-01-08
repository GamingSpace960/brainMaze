import numpy as np
import pygame as pg
import World
from time import sleep,time

class LeadBlob():
    def __init__(self,world,leadership=np.random.randint(1,50+1),mindSizeX = np.random.randint(5,245+1),mindSizeY = np.random.randint(5,185+1),speed = np.random.randint(1,5),qtable = []):
        #bounds (370,310)-(450,370)
        # max spots = (450,370)/2 = (225,185)
        self.world = world
        self.colorReset()
        self.scoreReset()
        self.reset()
        self.leadership = leadership
        self.mindSizeX = mindSizeX
        self.mindSizeY = mindSizeY
        self.speed = speed
        #self.mindSizeX = 245
        #self.mindSizeY = 185
        self.lr = .1
        if len(qtable) == 0:
            self.qTable()
        else:
            self.qtable = qtable
        

    def draw(self,world):
        pg.draw.rect(world.win,self.color,self.me)

    def qTable(self):
        self.qtable = np.random.rand(245,185,4)

    def Action(self,epsilon,world = None):
        if self.dead or self.won:
            if world != None:
                self.draw(world)
            return
        if 245-(self.me.x/2) < 0 or 185-(self.me.y/2) < 0:
            print(245-(self.me.x/2),185-(self.me.y/2),self.me.x,self.me.y)
        if np.random.random() > epsilon and len(self.qtable) > 245-(self.me.x/2) and len(self.qtable[int(245-(self.me.x/2))]) > 185-(self.me.y/2):
            self.action = np.argmax(self.qtable[int(245-(self.me.x/2))][int(185-(self.me.y/2))])
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
        if self.me.collidelist(self.world.walls) != -1 or (self.me.x,self.me.y) in self.beenList:
            self.dead = True
            score -= 20_000
        elif self.me.colliderect(self.world.goal):
            score += 40_000-2*self.time
            self.won = True
            self.dead = True
        self.beenList.append((self.me.x,self.me.y))
        score +=1
        self.score += score
        self.time+=1
        
        if not self.dead and len(self.qtable) > 245-(self.me.x/2) and len(self.qtable[int(245-(self.me.x/2))]) > 185-(self.me.y/2) and len(self.qtable) > x and len(self.qtable[x]) > y:
            self.qtable[x][y][self.action] += self.lr* ((1-.99)*score + .99*max(self.qtable[int(245-(self.me.x/2))][int(185-(self.me.y/2))]) - self.qtable[x][y][self.action])
        elif len(self.qtable) > x and len(self.qtable[x]) > y:
            self.qtable[x][y][self.action] += self.lr*( score - self.qtable[x][y][self.action])
        if world != None:
            self.draw(world)


    def reset(self):
        
        
        #print(self.avgScore,self.games,self.score)
        self.games+=1
        self.avgScore = (self.avgScore*(self.games-1) + self.score)/self.games
        #print(self.avgScore,self.games,self.score,2)
        x = np.random.randint(370/2,450/2+.5)*2
        y = np.random.randint(310/2,370/2+.5)*2
        self.me = pg.draw.rect(self.world.win,(10,10,200),(x,y,2,2))
        self.beenList = []
        self.dead = False
        self.won = False
        self.score = 0
        self.time = 0

    def scoreReset(self):
        self.score = 0
        self.avgScore = 0
        self.games = 0

    def colorReset(self):
        self.color = (100,100,200)

    def copy(self):
        return LeadBlob(world=self.world,leadership=self.leadership,mindSizeX = self.mindSizeX,mindSizeY = self.mindSizeY,speed = self.speed, qtable = self.qtable)

