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
        self.qTable()

    def qTable(self):
        self.qtable = np.random.rand(self.mindSizeX,self.mindSizeY,4)

    def Action(self,epsilon):
        if self.dead or self.won:
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
        if self.me.collidelist(self.world.walls) != -1:
            self.dead = True
            score -= 10_000
        elif self.me.colliderect(self.world.goal):
            score += 10_000-.5*self.time
            self.won = True
        elif (self.me.x,self.me.y) in self.beenList:
            score -= 10
        self.beenList.append((self.me.x,self.me.y))
        score +=1
        self.score += score
        self.time+=1
        self.qtable[x][y][self.action] += self.lr* (score + .999*max(self.qtable[int(245-(self.me.x/2))][int(185-(self.me.y/2))]) - self.qtable[x][y][self.action])

    def restart(self):
        x = np.random.randint(370/2,450/2+.5)*2
        y = np.random.randint(310/2,370/2+.5)*2
        self.me = pg.draw.rect(self.world.win,(10,10,200),(x,y,2,2))
        self.beenList = []
        self.dead = False
        self.won = False
        self.score = 0
        self.time = 0


        
world = World.World()
st = time()
bobs = [LeadBlob(world) for _ in range(1_000)]
print((time()-st))


epsilon = .7
epsilonDecay = .01
step = 0
game = 0
while True:
    while step < 10_000 and False in [bob.dead for bob in bobs]:
        for bob in bobs:
            bob.Action(epsilon)
        if game%10 ==0:
            world.draw()
            [pg.draw.rect(world.win,(10,10,200),bob.me) for bob in bobs]
            world.update()
        step+= 1

    print(epsilon,max([bob.score for bob in bobs]))  
    for bob in bobs:
            bob.restart()
    epsilon -= epsilon*epsilonDecay
    if epsilon < .0001:
        epsilon = 1
    step = 0
    
    game+=1
    done = False