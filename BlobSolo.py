import numpy as np
import pygame as pg
import World
from time import sleep,time

class LeadBlob():
    def __init__(self,world,leadership=np.random.randint(1,50+1),mindSizeX = 245,mindSizeY = 185,speed = np.random.randint(1,5),qtable = []):
        #bounds (370,310)-(450,370)
        # max spots = (450,370)/2 = (225,185)
        self.world = world
        self.colorReset()
        self.scoreReset()
        self.reset()
        self.leadership = leadership
        self.mindSizeX = mindSizeX
        self.mindSizeY = mindSizeY
        self.speed = speedself.lr = .1
        if len(qtable) == 0:
            self.qTable()
        else:
            self.qtable = qtable
        

    def draw(self,world):
        pg.draw.rect(world.win,self.color,self.me)

    def qTable(self):
        self.qtable = np.random.rand(245,185,4)

    def Action(self,epsilon,world = None):
        if self.dead:
            if world != None:
                self.draw(world)
            return
        if 245-(self.me.x/2) < 0 or 185-(self.me.y/2) < 0:
            print(245-(self.me.x/2),185-(self.me.y/2),self.me.x,self.me.y)
        if np.random.random() > epsilon and len(self.qtable) > 245-(self.me.x/2) and len(self.qtable[int(245-(self.me.x/2))]) > 185-(self.me.y/2):
            self.action = np.argmax(self.qtable[int(245-(self.me.x/2))][int(185-(self.me.y/2))])
        else:
            self.action = np.random.randint(4)

        self.x = int(245-(self.me.x/2))
        self.y = int(185-(self.me.y/2))
        
        if self.action == 0:
            self.me.move_ip(-2*self.speed,0)
        elif self.action == 1:
            self.me.move_ip(2*self.speed,0)
        elif self.action == 2:
            self.me.move_ip(0,-2*self.speed)
        else:
            self.me.move_ip(0,2*self.speed)
        self.tempScore = 0
        if self.me.collidelist(self.world.walls) != -1 or (self.me.x,self.me.y) in self.beenList:
            self.dead = 1
            self.tempScore -= 20_000
        elif self.me.colliderect(self.world.goal):
            self.tempScore += 40_000-2*self.time
            self.dead = 1
        self.beenList.append((self.me.x,self.me.y))
        self.tempScore +=1
        self.score += self.tempScore
        self.time+=1
        
        if not self.dead and self.mindSizeX > 245-(self.me.x/2) and self.mindSizeY > 185-(self.me.y/2) and self.mindSizeX > self.x and self.mindSizeY > self.y:
            self.qtable[self.x][self.y][self.action] += self.lr* ((1-.99)*self.tempScore + .99*max(self.qtable[int(245-(self.me.x/2))][int(185-(self.me.y/2))]) - self.qtable[self.x][self.y][self.action])
        if world != None:
            self.draw(world)

    def lastUpdate(self):
        if self.mindSizeX > self.x and self.mindSizeY > self.y:
            self.qtable[self.x][self.y][self.action] += self.lr*( self.tempScore - self.qtable[self.x][self.y][self.action])
        self.score += self.tempScore

    def reset(self):
        self.games+=1
        self.avgScore = (self.avgScore*(self.games-1) + self.score)/self.games
        #print(self.avgScore,self.games,self.score,2)
        x = np.random.randint(370/2,450/2+.5)*2
        y = np.random.randint(310/2,370/2+.5)*2
        self.me = pg.draw.rect(self.world.win,self.color,(x,y,2,2))
        self.beenList = []
        self.dead = 0
        self.won = 0
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

