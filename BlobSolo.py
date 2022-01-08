import numpy as np
import pygame as pg
import World
from time import sleep,time

class LeadBlob():
    def __init__(self,world,leadership=np.random.randint(1,50+1),mindSizeX = np.random.randint(1,239+1),mindSizeY = np.random.randint(1,179+1),speed = np.random.randint(1,6),qtable = []):
        #bounds (370,310)-(440,370)
        # max spots = (440,370)/2 = (220,185)
        # range is 5 -> 220 so -(-5) = +5 is needed for a 0 therefore max mind size is 215/180

        # map size = (10,10,480,360) = pixels = (10,10,490,370)
        # spawn size = (370,310,80,60) = pixels = (370,310,450,370)
        # bots only read top left of themselves so for bot minus 2 for high x & y
        # pixels is value read
        # map size = (10,10,478,358) = pixels = (10,10,488,368)
        # spawn size = (370,310,78,58) = pixels = (370,310,448,368)
        #mind size range = (5,5,244,184)
        #max mind size = (239,179)
        self.world = world
        self.colorReset()
        self.scoreReset()
        self.reset()
        self.leadership = leadership
        self.mindSizeX = mindSizeX
        self.mindSizeY = mindSizeY
        self.speed = speed
        self.lr = .1
        if len(qtable) == 0:
            self.qTable()
        else:
            self.qtable = qtable
        

    def draw(self,world):
        pg.draw.rect(world.win,self.color,self.me)

    def qTable(self):
        self.qtable = np.random.rand(239,179,4)

    def Action(self,epsilon,world = None):
        if self.dead or self.won:
            if world != None:
                self.draw(world)
            return
        if 244-(self.me.x/2) < 0 or 184-(self.me.y/2) < 0:
            print(244-(self.me.x/2),184-(self.me.y/2),self.me.x,self.me.y)
        if np.random.random() > epsilon and len(self.qtable) > 244-(self.me.x/2) and len(self.qtable[int(244-(self.me.x/2))]) > 184-(self.me.y/2):
            self.action = np.argmax(self.qtable[int(244-(self.me.x/2))][int(184-(self.me.y/2))])
        else:
            self.action = np.random.randint(4)

        x = int(244-(self.me.x/2))
        y = int(184-(self.me.y/2))
        
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
        
        if not self.dead and self.mindSizeX >= 244-(self.me.x/2) and self.mindSizeY >= 184-(self.me.y/2) and self.mindSizeX >= x and self.mindSizeY >= y:
            self.qtable[x][y][self.action] += self.lr* ((1-.99)*score + .99*max(self.qtable[int(244-(self.me.x/2))][int(184-(self.me.y/2))]) - self.qtable[x][y][self.action])
        elif self.mindSizeX >= x and self.mindSizeY >= y:
            self.qtable[x][y][self.action] += self.lr*( score - self.qtable[x][y][self.action])
        if world != None:
            self.draw(world)


    def reset(self):
        
        
        #print(self.avgScore,self.games,self.score)
        self.games+=1
        self.avgScore = (self.avgScore*(self.games-1) + self.score)/self.games
        #print(self.avgScore,self.games,self.score,2)
        x = np.random.randint(370/2,448/2+.5)*2
        y = np.random.randint(310/2,368/2+.5)*2
        self.me = pg.draw.rect(self.world.win,self.color,(x,y,2,2))
        self.beenList = []
        self.dead = False
        self.won = False
        self.score = 0
        self.time = 0

    def scoreReset(self):
        self.score = 0
        self.avgScore = 0
        self.games = 0
        x = np.random.randint(370/2,448/2+.5)*2
        y = np.random.randint(310/2,368/2+.5)*2
        self.me = pg.draw.rect(self.world.win,self.color,(x,y,2,2))

    def colorReset(self):
        self.color = (100,100,200)

    def copy(self):
        return LeadBlob(world=self.world,leadership=self.leadership,mindSizeX = self.mindSizeX,mindSizeY = self.mindSizeY,speed = self.speed, qtable = self.qtable)

